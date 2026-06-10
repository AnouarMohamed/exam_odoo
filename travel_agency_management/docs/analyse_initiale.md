# Analyse Initiale

## Ce que demande le cahier des charges

Le cahier des charges impose de concevoir un système d'information sous Odoo 17, avec un module spécifique installable, une intégration avec des modules standards, une modélisation BPMN, une documentation fonctionnelle et technique, un rapport académique en français, un manuel utilisateur avec captures, un rapport QWeb PDF, une sécurité par groupes et règles d'accès, du reporting graph/pivot, des données de démonstration et des tests de recette.

## Sujet spécifique

Le sujet réel est : **Gestion d’une agence de voyages**.

Le projet est donc centré sur Atlas Horizon Travel, une agence de voyages fictive qui vend des packages organisés, planifie des départs, gère des réservations, suit les voyageurs, contrôle la capacité, crée des devis et produit des bons de réservation.

## Module Odoo à créer

Le module spécifique est :

```text
travel_agency_management
```

Nom fonctionnel en français :

```text
Gestion d’une agence de voyages
```

## Modules standards réutilisés

- `contacts` : clients et prestataires.
- `sale_management` : devis et commandes de vente.
- `account` : facturation standard après confirmation des commandes.
- `mail` : chatter, suivi et activités sur les réservations.
- `base` : utilisateurs, sociétés, devises, pays et sécurité de base.

## Entités personnalisées nécessaires

- `travel.destination` : destinations touristiques.
- `travel.package` : packages commercialisés.
- `travel.departure` : départs programmés et capacité.
- `travel.booking` : réservations et workflow.
- `travel.passenger` : voyageurs rattachés aux réservations.

## Captures à produire

Les captures réelles attendues sont listées dans `scripts/screenshot_checklist.md` et doivent être enregistrées dans `docs/screenshots/`.

Elles couvrent le menu principal, les listes et formulaires des destinations, packages, départs, réservations, le devis Odoo, le bon PDF, les vues graph/pivot et les groupes de sécurité.

## Documentation à générer

- `docs/rapport_projet.md`
- `docs/manuel_utilisateur.md`
- `docs/modele_donnees.md`
- `docs/cahier_recette.md`
- `docs/checklist_finale.md`
- `README.md`
- BPMN dans `docs/bpmn/`
- Mermaid dans `docs/diagrams/`
