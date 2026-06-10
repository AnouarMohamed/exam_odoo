from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestTravelWorkflow(TransactionCase):
    def setUp(self):
        super().setUp()
        self.env.user.write(
            {
                "groups_id": [
                    (4, self.env.ref("travel_agency_management.group_travel_manager").id)
                ]
            }
        )
        self.country = self.env.ref("base.ma")
        self.customer = self.env["res.partner"].create(
            {
                "name": "Client Test Voyage",
                "email": "client.test@example.com",
                "customer_rank": 1,
            }
        )
        self.destination = self.env["travel.destination"].create(
            {
                "name": "Marrakech Test",
                "city": "Marrakech Test",
                "country_id": self.country.id,
            }
        )
        self.package = self.env["travel.package"].create(
            {
                "name": "Package Test Marrakech",
                "destination_id": self.destination.id,
                "duration_days": 3,
                "base_price": 500.0,
            }
        )
        self.package.action_publish()
        self.departure = self.env["travel.departure"].create(
            {
                "package_id": self.package.id,
                "departure_date": "2026-07-01",
                "capacity": 2,
            }
        )
        self.departure.action_open()

    def _create_booking(self, passenger_name="Voyageur Test", departure=None):
        departure = departure or self.departure
        return self.env["travel.booking"].create(
            {
                "customer_id": self.customer.id,
                "package_id": departure.package_id.id,
                "departure_id": departure.id,
                "passenger_ids": [
                    (
                        0,
                        0,
                        {
                            "name": passenger_name,
                            "date_of_birth": "1990-01-01",
                            "nationality_id": self.country.id,
                            "passport_number": "TEST123456",
                        },
                    )
                ],
            }
        )

    def test_complete_booking_workflow(self):
        booking = self._create_booking()

        self.assertTrue(self.destination)
        self.assertEqual(self.package.state, "published")
        self.assertEqual(self.departure.state, "open")
        self.assertEqual(booking.passenger_count, 1)

        booking.action_submit()
        self.assertEqual(booking.state, "submitted")

        booking.action_approve()
        self.assertEqual(booking.state, "approved")
        self.assertEqual(self.departure.booked_seats, 1)
        self.assertEqual(self.departure.available_seats, 1)

        booking.action_create_sale_order()
        self.assertEqual(booking.state, "sale_created")
        self.assertTrue(booking.sale_order_id)
        self.assertEqual(booking.sale_order_id.partner_id, self.customer)

        booking.action_confirm_booking()
        self.assertEqual(booking.state, "confirmed")
        self.assertIn(booking.sale_order_id.state, ("sale", "done"))

    def test_capacity_prevents_overbooking(self):
        limited_departure = self.env["travel.departure"].create(
            {
                "package_id": self.package.id,
                "departure_date": "2026-07-15",
                "capacity": 1,
            }
        )
        limited_departure.action_open()

        first_booking = self._create_booking(
            passenger_name="Premier Voyageur", departure=limited_departure
        )
        first_booking.action_submit()
        first_booking.action_approve()
        self.assertEqual(limited_departure.available_seats, 0)

        second_booking = self._create_booking(
            passenger_name="Deuxième Voyageur", departure=limited_departure
        )
        second_booking.action_submit()
        with self.assertRaises(UserError):
            second_booking.action_approve()
