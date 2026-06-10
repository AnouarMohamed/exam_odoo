from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class TravelBooking(models.Model):
    _name = "travel.booking"
    _description = "Réservation de voyage"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "booking_date desc, name desc"

    name = fields.Char(
        string="Référence",
        required=True,
        copy=False,
        readonly=True,
        default="Nouveau",
    )
    customer_id = fields.Many2one(
        "res.partner",
        string="Client",
        required=True,
        tracking=True,
        domain=[("type", "!=", "private")],
    )
    package_id = fields.Many2one(
        "travel.package", string="Package", required=True, tracking=True
    )
    departure_id = fields.Many2one(
        "travel.departure", string="Départ", required=True, tracking=True
    )
    destination_id = fields.Many2one(
        "travel.destination",
        string="Destination",
        related="departure_id.destination_id",
        store=True,
        readonly=True,
    )
    departure_capacity = fields.Integer(
        string="Capacité du départ", related="departure_id.capacity", readonly=True
    )
    departure_available_seats = fields.Integer(
        string="Places disponibles", related="departure_id.available_seats", readonly=True
    )
    booking_date = fields.Date(
        string="Date de réservation", default=fields.Date.context_today, required=True
    )
    passenger_ids = fields.One2many(
        "travel.passenger", "booking_id", string="Voyageurs", copy=True
    )
    passenger_count = fields.Integer(
        string="Nombre de voyageurs", compute="_compute_passenger_count", store=True
    )
    unit_price = fields.Monetary(string="Prix unitaire", tracking=True)
    discount_amount = fields.Monetary(string="Remise")
    total_amount = fields.Monetary(
        string="Montant total", compute="_compute_total_amount", store=True, tracking=True
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Devise",
        required=True,
        default=lambda self: self.env.company.currency_id.id,
    )
    responsible_user_id = fields.Many2one(
        "res.users",
        string="Responsable",
        default=lambda self: self.env.user.id,
        tracking=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Société",
        required=True,
        default=lambda self: self.env.company.id,
    )
    sale_order_id = fields.Many2one(
        "sale.order", string="Devis / Commande", readonly=True, copy=False
    )
    invoice_count = fields.Integer(string="Factures", compute="_compute_invoice_count")
    note = fields.Text(string="Notes")
    cancellation_reason = fields.Text(string="Motif d'annulation")
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("submitted", "Soumise"),
            ("approved", "Approuvée"),
            ("sale_created", "Devis créé"),
            ("confirmed", "Confirmée"),
            ("done", "Terminée"),
            ("cancelled", "Annulée"),
        ],
        string="Statut",
        default="draft",
        tracking=True,
        required=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._check_state_values(vals)
            if vals.get("name", "Nouveau") in ("New", "Nouveau"):
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("travel.booking") or "Nouveau"
                )
            package = self.env["travel.package"].browse(vals.get("package_id"))
            if package:
                vals.setdefault("unit_price", package.base_price)
                vals.setdefault("currency_id", package.currency_id.id)
        return super().create(vals_list)

    def write(self, vals):
        self._check_state_values(vals)
        return super().write(vals)

    def _check_state_values(self, vals):
        target_state = vals.get("state")
        if not target_state:
            return
        if not self and not self.env.su and target_state != "draft":
            raise UserError(
                _("Une réservation doit être créée en brouillon puis suivre le workflow.")
            )
        if (
            target_state == "approved"
            and not self.env.su
            and not self.env.user.has_group(
                "travel_agency_management.group_travel_manager"
            )
        ):
            raise AccessError(_("Seul un responsable peut approuver une réservation."))
        if target_state == "approved":
            for booking in self:
                if booking.state != "submitted":
                    raise UserError(_("Seules les réservations soumises peuvent être approuvées."))
            self._ensure_capacity_available()
        if target_state == "sale_created":
            if not self and not vals.get("sale_order_id"):
                raise UserError(_("Un devis est obligatoire pour passer à l'état Devis créé."))
            for booking in self:
                sale_order_id = vals.get("sale_order_id") or booking.sale_order_id.id
                if not sale_order_id:
                    raise UserError(_("Un devis est obligatoire pour passer à l'état Devis créé."))
        if target_state == "confirmed":
            if not self and not vals.get("sale_order_id"):
                raise UserError(_("Un devis est obligatoire pour confirmer la réservation."))
            for booking in self:
                sale_order_id = vals.get("sale_order_id") or booking.sale_order_id.id
                if not sale_order_id:
                    raise UserError(_("Un devis est obligatoire pour confirmer la réservation."))

    @api.depends("passenger_ids", "passenger_ids.name")
    def _compute_passenger_count(self):
        for booking in self:
            booking.passenger_count = len(booking.passenger_ids)

    @api.depends("unit_price", "discount_amount", "passenger_count")
    def _compute_total_amount(self):
        for booking in self:
            subtotal = (booking.unit_price or 0.0) * booking.passenger_count
            booking.total_amount = max(subtotal - (booking.discount_amount or 0.0), 0.0)

    def _compute_invoice_count(self):
        for booking in self:
            booking.invoice_count = (
                len(booking.sale_order_id.invoice_ids) if booking.sale_order_id else 0
            )

    @api.onchange("package_id")
    def _onchange_package_id(self):
        if self.package_id:
            self.unit_price = self.package_id.base_price
            self.currency_id = self.package_id.currency_id
            return {
                "domain": {
                    "departure_id": [
                        ("package_id", "=", self.package_id.id),
                        ("state", "=", "open"),
                    ]
                }
            }
        return {"domain": {"departure_id": []}}

    @api.onchange("departure_id")
    def _onchange_departure_id(self):
        if self.departure_id:
            self.package_id = self.departure_id.package_id
            self.unit_price = self.departure_id.package_id.base_price
            self.currency_id = self.departure_id.package_id.currency_id

    @api.constrains("unit_price", "discount_amount")
    def _check_amounts(self):
        for booking in self:
            if booking.unit_price < 0:
                raise ValidationError(_("Le prix unitaire ne peut pas être négatif."))
            if booking.discount_amount < 0:
                raise ValidationError(_("La remise ne peut pas être négative."))

    @api.constrains("package_id", "departure_id")
    def _check_departure_package(self):
        for booking in self:
            if (
                booking.package_id
                and booking.departure_id
                and booking.departure_id.package_id != booking.package_id
            ):
                raise ValidationError(
                    _("Le départ sélectionné doit appartenir au package choisi.")
                )

    def _ensure_can_submit(self):
        for booking in self:
            if not booking.customer_id or not booking.package_id or not booking.departure_id:
                raise UserError(
                    _("Le client, le package et le départ sont obligatoires.")
                )
            if not booking.passenger_ids:
                raise UserError(_("Ajoutez au moins un voyageur avant de soumettre."))
            if booking.departure_id.state != "open":
                raise UserError(_("Le départ doit être ouvert pour accepter une réservation."))

    def _ensure_capacity_available(self):
        for booking in self:
            if booking.passenger_count <= 0:
                raise UserError(_("La réservation doit contenir au moins un voyageur."))
            if booking.departure_id.available_seats < booking.passenger_count:
                raise UserError(
                    _(
                        "Places insuffisantes sur ce départ. Disponibles: %(available)s, demandées: %(requested)s."
                    )
                    % {
                        "available": booking.departure_id.available_seats,
                        "requested": booking.passenger_count,
                    }
                )

    def action_submit(self):
        for booking in self:
            if booking.state != "draft":
                raise UserError(_("Seules les réservations en brouillon peuvent être soumises."))
        self._ensure_can_submit()
        self.write({"state": "submitted"})

    def action_approve(self):
        if not self.env.user.has_group(
            "travel_agency_management.group_travel_manager"
        ):
            raise AccessError(_("Seul un responsable peut approuver une réservation."))
        for booking in self:
            if booking.state != "submitted":
                raise UserError(_("Seules les réservations soumises peuvent être approuvées."))
            if booking.departure_id.state != "open":
                raise UserError(_("Le départ doit être ouvert pour approuver la réservation."))
            booking._ensure_capacity_available()
            booking.write({"state": "approved"})

    def _get_travel_product(self):
        product_template = self.env["product.template"].sudo().search(
            [("default_code", "=", "TRAVEL_ORGANISE")], limit=1
        )
        if not product_template:
            product_template = self.env["product.template"].sudo().create(
                {
                    "name": "Voyage organisé",
                    "default_code": "TRAVEL_ORGANISE",
                    "detailed_type": "service",
                    "sale_ok": True,
                    "purchase_ok": False,
                    "invoice_policy": "order",
                }
            )
        return product_template.product_variant_id

    def action_create_sale_order(self):
        SaleOrder = self.env["sale.order"]
        for booking in self:
            if booking.state != "approved":
                raise UserError(_("La réservation doit être approuvée avant de créer un devis."))
            if booking.sale_order_id:
                raise UserError(_("Un devis existe déjà pour cette réservation."))
            if booking.passenger_count <= 0:
                raise UserError(_("Ajoutez au moins un voyageur avant de créer le devis."))

            product = booking._get_travel_product()
            line_description = _(
                "%(package)s - %(destination)s\nDépart: %(departure)s\nVoyageurs: %(count)s"
            ) % {
                "package": booking.package_id.name,
                "destination": booking.destination_id.display_name,
                "departure": fields.Date.to_string(booking.departure_id.departure_date),
                "count": booking.passenger_count,
            }
            sale_order = SaleOrder.create(
                {
                    "partner_id": booking.customer_id.id,
                    "company_id": booking.company_id.id,
                    "origin": booking.name,
                    "client_order_ref": booking.name,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "name": line_description,
                                "product_uom_qty": booking.passenger_count,
                                "price_unit": booking.unit_price,
                            },
                        )
                    ],
                }
            )
            booking.write({"sale_order_id": sale_order.id, "state": "sale_created"})
            booking.message_post(
                body=_("Devis %(order)s créé depuis la réservation.") % {
                    "order": sale_order.name
                }
            )

    def action_confirm_booking(self):
        for booking in self:
            if booking.state != "sale_created":
                raise UserError(_("Le devis doit être créé avant la confirmation."))
            if not booking.sale_order_id:
                raise UserError(_("Aucun devis n'est lié à cette réservation."))
            if booking.sale_order_id.state == "cancel":
                raise UserError(_("Le devis lié est annulé et ne peut pas confirmer la réservation."))
            if booking.sale_order_id.state in ("draft", "sent"):
                booking.sale_order_id.action_confirm()
            booking.state = "confirmed"
            booking.message_post(body=_("Réservation confirmée."))

    def action_done(self):
        for booking in self:
            if booking.state != "confirmed":
                raise UserError(_("Seules les réservations confirmées peuvent être terminées."))
        self.write({"state": "done"})

    def action_cancel(self):
        for booking in self:
            if booking.state == "done":
                raise UserError(_("Une réservation terminée ne peut pas être annulée."))
        self.write({"state": "cancelled"})

    def action_reset_to_draft(self):
        for booking in self:
            if booking.state not in ("cancelled", "submitted"):
                raise UserError(
                    _("Seules les réservations annulées ou soumises peuvent être remises en brouillon.")
                )
        self.write({"state": "draft", "cancellation_reason": False})

    def action_view_sale_order(self):
        self.ensure_one()
        if not self.sale_order_id:
            raise UserError(_("Aucun devis n'est lié à cette réservation."))
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_orders")
        action["views"] = [(False, "form")]
        action["res_id"] = self.sale_order_id.id
        return action

    def action_print_booking_report(self):
        return self.env.ref(
            "travel_agency_management.action_report_travel_booking"
        ).report_action(self)

    def _get_state_label(self):
        self.ensure_one()
        return dict(self._fields["state"].selection).get(self.state, self.state)
