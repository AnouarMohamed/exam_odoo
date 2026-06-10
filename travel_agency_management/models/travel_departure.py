from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class TravelDeparture(models.Model):
    _name = "travel.departure"
    _description = "Départ programmé"
    _order = "departure_date desc, package_id"

    name = fields.Char(string="Référence", compute="_compute_name", store=True)
    package_id = fields.Many2one(
        "travel.package", string="Package", required=True, ondelete="restrict"
    )
    destination_id = fields.Many2one(
        "travel.destination",
        string="Destination",
        related="package_id.destination_id",
        store=True,
        readonly=True,
    )
    departure_date = fields.Date(string="Date de départ", required=True)
    return_date = fields.Date(
        string="Date de retour", compute="_compute_return_date", store=True, readonly=False
    )
    capacity = fields.Integer(string="Capacité", required=True, default=20)
    booked_seats = fields.Integer(string="Places réservées", compute="_compute_seats")
    available_seats = fields.Integer(string="Places disponibles", compute="_compute_seats")
    booking_ids = fields.One2many("travel.booking", "departure_id", string="Réservations")
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("open", "Ouvert"),
            ("closed", "Fermé"),
            ("cancelled", "Annulé"),
        ],
        string="Statut",
        default="draft",
        required=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Société",
        required=True,
        default=lambda self: self.env.company.id,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Devise",
        related="package_id.currency_id",
        store=True,
        readonly=True,
    )

    @api.depends("package_id", "departure_date", "return_date")
    def _compute_name(self):
        for departure in self:
            if departure.package_id and departure.departure_date:
                departure.name = "%s - %s" % (
                    departure.package_id.name,
                    fields.Date.to_string(departure.departure_date),
                )
            elif departure.package_id:
                departure.name = departure.package_id.name
            else:
                departure.name = _("Nouveau départ")

    @api.depends("departure_date", "package_id.duration_days")
    def _compute_return_date(self):
        for departure in self:
            if departure.departure_date and departure.package_id:
                duration = max(departure.package_id.duration_days or 1, 1)
                departure.return_date = fields.Date.add(
                    departure.departure_date, days=duration - 1
                )
            elif not departure.return_date:
                departure.return_date = departure.departure_date

    @api.depends("booking_ids.state", "booking_ids.passenger_count", "capacity")
    def _compute_seats(self):
        counted_states = ["approved", "sale_created", "confirmed", "done"]
        for departure in self:
            booked = sum(
                booking.passenger_count
                for booking in departure.booking_ids
                if booking.state in counted_states
            )
            departure.booked_seats = booked
            departure.available_seats = departure.capacity - booked

    @api.constrains("departure_date", "return_date")
    def _check_dates(self):
        for departure in self:
            if (
                departure.departure_date
                and departure.return_date
                and departure.return_date < departure.departure_date
            ):
                raise ValidationError(
                    _("La date de retour doit être postérieure ou égale à la date de départ.")
                )

    @api.constrains("capacity")
    def _check_capacity(self):
        for departure in self:
            if departure.capacity <= 0:
                raise ValidationError(_("La capacité doit être supérieure à 0."))
            active_passengers = sum(
                booking.passenger_count
                for booking in departure.booking_ids
                if booking.state in ("approved", "sale_created", "confirmed", "done")
            )
            if active_passengers > departure.capacity:
                raise ValidationError(
                    _(
                        "La capacité ne peut pas être inférieure aux places déjà réservées (%(count)s)."
                    )
                    % {"count": active_passengers}
                )

    def action_open(self):
        for departure in self:
            if departure.package_id.state != "published":
                raise UserError(
                    _("Vous devez publier le package avant d'ouvrir ce départ.")
                )
            if departure.capacity <= 0:
                raise UserError(_("La capacité du départ doit être supérieure à 0."))
            departure.state = "open"

    def action_close(self):
        self.write({"state": "closed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_reset_to_draft(self):
        self.write({"state": "draft"})
