# Manuel Utilisateur

## Objectif

Ce manuel explique l'utilisation du module Odoo 17 `Gestion d’une agence de voyages` développé pour Atlas Horizon Travel. Il couvre la gestion des destinations, packages, départs, réservations, voyageurs, devis, reporting et bon de réservation.

Les captures d'écran attendues doivent être générées dans `docs/screenshots/` avec le script `scripts/take_screenshots.py` après installation du module dans une base Odoo 17 réelle.

## Accès au module

Après installation, ouvrir le menu principal :

![Menu principal](screenshots/01_menu_principal.png)

Le menu `Agence de Voyages` contient :

- Réservations ;
- Voyages > Destinations ;
- Voyages > Packages ;
- Voyages > Départs ;
- Voyageurs ;
- Reporting > Analyse des réservations.

## Gestion des destinations

Ouvrir `Agence de Voyages > Voyages > Destinations`.

![Liste des destinations](screenshots/02_liste_destinations.png)

Créer une destination avec un nom, un pays, une ville, une description et éventuellement une image.

![Formulaire destination](screenshots/03_formulaire_destination.png)

Le système empêche la création de deux destinations ayant la même ville dans le même pays.

## Gestion des packages

Ouvrir `Agence de Voyages > Voyages > Packages`.

![Liste des packages](screenshots/04_liste_packages.png)

Créer un package en renseignant la destination, la durée, le prix de base, la devise, les services inclus et les prestataires.

![Formulaire package](screenshots/05_formulaire_package.png)

Un package doit être publié avant de pouvoir ouvrir un départ. Le bouton `Publier` passe le package à l'état `Publié`.

## Gestion des départs

Ouvrir `Agence de Voyages > Voyages > Départs`.

![Liste des départs](screenshots/06_liste_departs.png)

Créer un départ en choisissant un package publié, une date de départ et une capacité.

![Formulaire départ](screenshots/07_formulaire_depart.png)

Cliquer sur `Ouvrir` pour rendre le départ disponible à la réservation. Les champs `Places réservées` et `Places disponibles` sont calculés automatiquement.

## Gestion des réservations

Ouvrir `Agence de Voyages > Réservations`.

![Liste des réservations](screenshots/08_liste_reservations.png)

Créer une réservation en renseignant le client, le package, le départ et les voyageurs.

![Réservation brouillon](screenshots/09_reservation_brouillon.png)

Cliquer sur `Soumettre` lorsque la réservation est complète.

![Réservation soumise](screenshots/10_reservation_soumise.png)

Un responsable agence clique ensuite sur `Approuver`. Le système vérifie la capacité disponible avant de valider l'approbation.

![Réservation approuvée](screenshots/11_reservation_approuvee.png)

## Création du devis

Depuis une réservation approuvée, cliquer sur `Créer le devis`.

![Devis Odoo](screenshots/12_devis_odoo.png)

Odoo crée un devis standard avec :

- le client de la réservation ;
- une ligne de service `Voyage organisé` ;
- le prix unitaire du package ;
- la quantité égale au nombre de voyageurs ;
- une description contenant package, destination et date de départ.

## Confirmation de réservation

Après création du devis, cliquer sur `Confirmer la réservation`.

![Réservation confirmée](screenshots/13_reservation_confirmee.png)

La réservation passe à l'état `Confirmée`. La facturation est ensuite réalisée par le fonctionnement standard d'Odoo Ventes et Facturation/Comptabilité.

## Bon de réservation

Cliquer sur `Imprimer le bon` depuis une réservation approuvée, avec devis créé ou confirmée.

![Bon de réservation PDF](screenshots/14_bon_reservation_pdf.png)

Le PDF contient les informations de l'agence, du client, du voyage, des voyageurs, des montants et des conditions.

## Reporting

Ouvrir `Agence de Voyages > Reporting > Analyse des réservations`.

Vue graph :

![Vue graph réservations](screenshots/15_vue_graph_reservations.png)

Vue pivot :

![Vue pivot réservations](screenshots/16_vue_pivot_reservations.png)

Ces vues permettent d'analyser les réservations par destination, package, statut et mois.

## Sécurité

Deux groupes sont disponibles :

- `Utilisateur Agence de Voyages` ;
- `Responsable Agence de Voyages`.

![Groupes de sécurité](screenshots/17_groupes_securite.png)

Un utilisateur simple gère ses propres réservations. Un responsable voit toutes les réservations et peut approuver.

## Règles métier importantes

- Une réservation ne peut pas être soumise sans client, package, départ et voyageur.
- Une réservation ne peut pas être soumise si le départ n'est pas ouvert.
- Seul un responsable peut approuver.
- L'approbation est bloquée si les places disponibles sont insuffisantes.
- Une réservation annulée ne consomme pas de capacité.
- Un devis ne peut pas être créé deux fois pour la même réservation.
- Une réservation ne peut pas être confirmée sans devis.
