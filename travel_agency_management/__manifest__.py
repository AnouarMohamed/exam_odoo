{
    "name": "Gestion d’une agence de voyages",
    "version": "17.0.1.0.0",
    "category": "Services/Travel",
    "summary": "SI Odoo 17 pour la gestion d'une agence de voyages.",
    "description": """
Gestion d’une agence de voyages
================================

Module métier pour Atlas Horizon Travel : destinations, packages,
départs, réservations, voyageurs, capacité, devis de vente, reporting
et bon de réservation PDF.
    """,
    "author": "Atlas Horizon Travel",
    "website": "https://example.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "contacts",
        "sale_management",
        "account",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "security/record_rules.xml",
        "data/sequence.xml",
        "data/demo_data.xml",
        "views/travel_departure_views.xml",
        "views/travel_package_views.xml",
        "views/travel_destination_views.xml",
        "views/travel_booking_views.xml",
        "views/travel_passenger_views.xml",
        "views/reporting_views.xml",
        "views/travel_menus.xml",
        "reports/booking_report.xml",
        "reports/booking_report_templates.xml",
    ],
    "application": True,
    "installable": True,
}
