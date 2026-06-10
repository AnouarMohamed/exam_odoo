import re

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TravelPassenger(models.Model):
    _name = "travel.passenger"
    _description = "Voyageur"
    _order = "name"

    name = fields.Char(string="Nom complet", required=True)
    booking_id = fields.Many2one(
        "travel.booking",
        string="Réservation",
        required=True,
        ondelete="cascade",
    )
    date_of_birth = fields.Date(string="Date de naissance")
    passport_number = fields.Char(string="Numéro de passeport")
    nationality_id = fields.Many2one("res.country", string="Nationalité")
    phone = fields.Char(string="Téléphone")
    email = fields.Char(string="Email")
    age = fields.Integer(string="Âge", compute="_compute_age")
    notes = fields.Text(string="Notes")

    @api.depends("date_of_birth")
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for passenger in self:
            if passenger.date_of_birth:
                passenger.age = (
                    today.year
                    - passenger.date_of_birth.year
                    - (
                        (today.month, today.day)
                        < (passenger.date_of_birth.month, passenger.date_of_birth.day)
                    )
                )
            else:
                passenger.age = 0

    @api.constrains("email")
    def _check_email(self):
        pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        for passenger in self:
            if passenger.email and not pattern.match(passenger.email):
                raise ValidationError(_("L'adresse email du voyageur n'est pas valide."))
