# Captures d'écran

Ce dossier est réservé aux captures réelles de l'application Odoo 17 après installation du module `travel_agency_management`.

Aucune image factice ne doit être placée ici. Les captures doivent être produites avec une base Odoo fonctionnelle contenant les données de démonstration du module.

Commande recommandée depuis la racine du module :

```bash
pip install playwright
playwright install chromium
ODOO_URL=http://localhost:8069 ODOO_LOGIN=admin ODOO_PASSWORD=admin python scripts/take_screenshots.py
```

Le script génère les fichiers attendus :

1. `01_menu_principal.png`
2. `02_liste_destinations.png`
3. `03_formulaire_destination.png`
4. `04_liste_packages.png`
5. `05_formulaire_package.png`
6. `06_liste_departs.png`
7. `07_formulaire_depart.png`
8. `08_liste_reservations.png`
9. `09_reservation_brouillon.png`
10. `10_reservation_soumise.png`
11. `11_reservation_approuvee.png`
12. `12_devis_odoo.png`
13. `13_reservation_confirmee.png`
14. `14_bon_reservation_pdf.png`
15. `15_vue_graph_reservations.png`
16. `16_vue_pivot_reservations.png`
17. `17_groupes_securite.png`
