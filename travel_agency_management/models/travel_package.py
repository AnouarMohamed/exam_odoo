from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TravelPackage(models.Model):
    _name = "travel.package"
    _description = "Package de voyage"
    _order = "name"

    name = fields.Char(string="Nom du package", required=True)
    destination_id = fields.Many2one(
        "travel.destination", string="Destination", required=True, ondelete="restrict"
    )
    duration_days = fields.Integer(string="Durée (jours)", required=True, default=1)
    description = fields.Html(string="Description")
    base_price = fields.Monetary(string="Prix de base", required=True)
    currency_id = fields.Many2one(
        "res.currency",
        string="Devise",
        required=True,
        default=lambda self: self.env.company.currency_id.id,
    )
    included_services = fields.Text(string="Services inclus")
    supplier_ids = fields.Many2many(
        "res.partner",
        "travel_package_supplier_rel",
        "package_id",
        "partner_id",
        string="Prestataires",
        domain=[("supplier_rank", ">", 0)],
    )
    departure_ids = fields.One2many("travel.departure", "package_id", string="Départs")
    image_1920 = fields.Image(string="Image")
    active = fields.Boolean(string="Actif", default=True)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("published", "Publié"),
            ("archived", "Archivé"),
        ],
        string="Statut",
        default="draft",
        required=True,
    )
    booking_count = fields.Integer(string="Réservations", compute="_compute_counts")
    departure_count = fields.Integer(string="Départs", compute="_compute_counts")

    def _compute_counts(self):
        Booking = self.env["travel.booking"]
        for package in self:
            package.departure_count = len(package.departure_ids)
            package.booking_count = Booking.search_count(
                [
                    ("package_id", "=", package.id),
                    ("state", "!=", "cancelled"),
                ]
            )

    @api.constrains("duration_days")
    def _check_duration_days(self):
        for package in self:
            if package.duration_days <= 0:
                raise ValidationError(_("La durée doit être supérieure à 0 jour."))

    @api.constrains("base_price")
    def _check_base_price(self):
        for package in self:
            if package.base_price < 0:
                raise ValidationError(_("Le prix de base ne peut pas être négatif."))

    def action_publish(self):
        for package in self:
            if not package.destination_id:
                raise ValidationError(_("Un package publié doit avoir une destination."))
            package.write({"state": "published", "active": True})

    def action_archive_package(self):
        self.write({"state": "archived", "active": False})

    def action_unarchive_package(self):
        self.write({"state": "draft", "active": True})
