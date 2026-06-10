# Gestion d’une agence de voyages

## Sujet

Conception et implémentation d'un système d'information sous Odoo 17 pour une agence de voyages fictive : **Atlas Horizon Travel**.

## Description

Le module `travel_agency_management` centralise la gestion des destinations, packages, départs programmés, réservations, voyageurs, devis, capacité, reporting et bons de réservation PDF.

Le projet est volontairement orienté métier voyage. Il ne s'agit pas d'un module générique de gestion d'entreprise.

## Périmètre fonctionnel

- Gestion des destinations touristiques.
- Gestion des packages de voyage.
- Gestion des prestataires liés aux packages.
- Planification des départs avec capacité.
- Gestion des réservations et voyageurs.
- Workflow : brouillon, soumise, approuvée, devis créé, confirmée, terminée, annulée.
- Contrôle de disponibilité et prévention du surbooking.
- Création d'un devis Odoo standard.
- Facturation via les modules standards Odoo.
- Bon de réservation QWeb PDF.
- Reporting graph et pivot.
- Groupes de sécurité agent/responsable.
- Données de démonstration réalistes.
- Tests automatisés Odoo du workflow.
- Documentation académique, BPMN et manuel utilisateur.

## Stack technique

- Odoo 17
- Python ORM Odoo
- XML views/actions/reports/security
- QWeb PDF
- Mermaid
- BPMN XML
- Playwright pour les captures d'écran

## Dépendances Odoo

Le manifeste déclare :

- `base`
- `mail`
- `contacts`
- `sale_management`
- `account`

## Installation

1. Copier le dossier `travel_agency_management` dans un chemin d'addons Odoo 17.
2. Redémarrer Odoo.
3. Activer le mode développeur.
4. Mettre à jour la liste des applications.
5. Installer **Gestion d’une agence de voyages**.
6. Ouvrir le menu **Agence de Voyages**.

Commande possible :

```bash
odoo-bin -d travel_agency_test -i travel_agency_management --stop-after-init
```

## Mise à jour

Après modification du module :

```bash
odoo-bin -d travel_agency_test -u travel_agency_management --stop-after-init
```

## Test du workflow

1. Ouvrir `Agence de Voyages > Voyages > Destinations`.
2. Vérifier les destinations de démonstration : Istanbul, Paris, Marrakech, Dubai.
3. Ouvrir `Voyages > Packages` et vérifier les packages publiés.
4. Ouvrir `Voyages > Départs` et vérifier les départs ouverts.
5. Créer une réservation avec client, package, départ et voyageurs.
6. Cliquer sur `Soumettre`.
7. Avec un responsable, cliquer sur `Approuver`.
8. Cliquer sur `Créer le devis`.
9. Ouvrir le devis Odoo généré.
10. Cliquer sur `Confirmer la réservation`.
11. Imprimer le `Bon de réservation`.
12. Vérifier que les places disponibles diminuent seulement après approbation.

## Tests automatisés

Les tests sont dans :

```text
tests/test_travel_workflow.py
```

Ils couvrent la création des objets métier, le workflow complet, la création du devis et le blocage du surbooking.

## Captures d'écran

Le script est disponible ici :

```text
scripts/take_screenshots.py
```

Commande :

```bash
pip install playwright
playwright install chromium
ODOO_URL=http://localhost:8069 ODOO_LOGIN=admin ODOO_PASSWORD=admin python scripts/take_screenshots.py
```

Les captures sont générées dans :

```text
docs/screenshots/
```

Le script ne crée pas d'images factices. Il nécessite une instance Odoo 17 démarrée, le module installé et les données de démonstration chargées.

## Documentation

- Rapport projet : `docs/rapport_projet.md`
- Analyse initiale : `docs/analyse_initiale.md`
- Manuel utilisateur : `docs/manuel_utilisateur.md`
- Modèle de données : `docs/modele_donnees.md`
- Cahier de recette : `docs/cahier_recette.md`
- Checklist finale : `docs/checklist_finale.md`
- BPMN : `docs/bpmn/`
- Diagrammes Mermaid : `docs/diagrams/`

## Limitations connues

- Le module ne crée pas de processus d'achat complet ; les prestataires sont gérés comme fournisseurs Odoo liés aux packages.
- La facturation est volontairement laissée au standard Odoo Ventes/Facturation.
- Les captures d'écran doivent être générées dans un environnement Odoo réel ; elles ne sont pas simulées.
- Les fichiers BPMN sont simplifiés pour documenter le processus métier. Les Mermaid fournissent une lecture visuelle rapide.

## Checklist académique finale

| Exigence | Statut |
| --- | --- |
| Cahier des charges traité comme instructions générales | Couvert |
| Sujet spécifique “Gestion d’une agence de voyages” traité comme sujet réel | Couvert |
| Projet orienté agence de voyages, non générique | Couvert |
| Module `travel_agency_management` créé | Couvert |
| Manifeste Odoo 17 avec dépendances standards | Couvert |
| Modèles destination, package, départ, réservation, voyageur | Couvert |
| Workflow réservation complet | Couvert |
| Contrôle de capacité et surbooking | Couvert |
| Création de devis Odoo standard | Couvert |
| Facturation standard documentée | Couvert |
| QWeb PDF “Bon de réservation” | Couvert |
| Groupes de sécurité agent/responsable | Couvert |
| Règles d'enregistrement | Couvert |
| Vues list/form/search/kanban | Couvert |
| Vues graph/pivot | Couvert |
| Données de démonstration | Couvert |
| Tests automatisés Odoo | Couvert |
| Deux processus BPMN | Couvert |
| Diagrammes Mermaid | Couvert |
| Rapport projet en français | Couvert |
| Manuel utilisateur en français | Couvert |
| Cahier de recette | Couvert |
| Script de captures d'écran | Couvert |
| Captures réelles | À générer dans un environnement Odoo lancé |
