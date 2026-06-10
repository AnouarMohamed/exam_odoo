from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TravelDestination(models.Model):
    _name = "travel.destination"
    _description = "Destination de voyage"
    _order = "country_id, city, name"

    name = fields.Char(string="Nom", required=True, index=True)
    country_id = fields.Many2one("res.country", string="Pays", required=True)
    city = fields.Char(string="Ville")
    description = fields.Text(string="Description")
    image_1920 = fields.Image(string="Image")
    active = fields.Boolean(string="Actif", default=True)
    package_ids = fields.One2many("travel.package", "destination_id", string="Packages")
    package_count = fields.Integer(string="Nombre de packages", compute="_compute_counts")
    departure_count = fields.Integer(string="Nombre de départs", compute="_compute_counts")
    booking_count = fields.Integer(string="Nombre de réservations", compute="_compute_counts")

    @api.depends("name", "city", "country_id")
    def _compute_display_name(self):
        for destination in self:
            parts = []
            if destination.city:
                parts.append(destination.city)
            parts.append(destination.name)
            if destination.country_id:
                parts.append(destination.country_id.name)
            destination.display_name = " - ".join(parts)

    def _compute_counts(self):
        Departure = self.env["travel.departure"]
        Booking = self.env["travel.booking"]
        for destination in self:
            destination.package_count = len(destination.package_ids)
            destination.departure_count = Departure.search_count(
                [("destination_id", "=", destination.id)]
            )
            destination.booking_count = Booking.search_count(
                [
                    ("destination_id", "=", destination.id),
                    ("state", "!=", "cancelled"),
                ]
            )

    @api.constrains("city", "country_id")
    def _check_unique_city_country(self):
        for destination in self:
            if not destination.city or not destination.country_id:
                continue
            duplicate = self.search_count(
                [
                    ("id", "!=", destination.id),
                    ("country_id", "=", destination.country_id.id),
                    ("city", "=ilike", destination.city.strip()),
                ]
            )
            if duplicate:
                raise ValidationError(
                    _(
                        "Une destination existe déjà pour la ville %(city)s dans le pays %(country)s."
                    )
                    % {
                        "city": destination.city,
                        "country": destination.country_id.name,
                    }
                )
