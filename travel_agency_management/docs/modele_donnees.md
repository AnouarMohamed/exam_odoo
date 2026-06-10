# Modèle de Données

## Vue générale

Le module `travel_agency_management` structure le système d'information d'Atlas Horizon Travel autour de cinq entités métier : destination, package, départ, réservation et voyageur. Ces entités sont reliées aux objets standards Odoo `res.partner`, `sale.order`, `res.users`, `res.company`, `res.currency` et `res.country`.

Le diagramme Mermaid est disponible dans `docs/diagrams/modele_donnees.mmd`.

## Entités métier

### Destination

Le modèle `travel.destination` représente une destination touristique commercialisée par l'agence. Il contient le nom, le pays, la ville, une description, une image et des compteurs de packages, départs et réservations.

Règle principale : une même ville ne doit pas être créée deux fois pour le même pays.

### Package

Le modèle `travel.package` représente une offre vendable : destination, durée, prix de base, services inclus, prestataires et statut de publication. Un package doit être publié avant l'ouverture d'un départ.

Règles principales :

- la durée doit être supérieure à zéro ;
- le prix de base ne peut pas être négatif ;
- les prestataires sont des contacts Odoo avec `supplier_rank > 0`.

### Départ

Le modèle `travel.departure` représente une date de départ planifiée pour un package. Il contient la capacité, les places réservées, les places disponibles, la date de départ, la date de retour et le statut.

Règles principales :

- la capacité doit être positive ;
- la date de retour doit être postérieure ou égale à la date de départ ;
- les places réservées ne prennent en compte que les réservations approuvées, avec devis créé, confirmées ou terminées ;
- les réservations annulées, brouillon ou soumises ne consomment pas de capacité.

### Réservation

Le modèle `travel.booking` pilote le workflow métier de réservation. Il hérite de `mail.thread` et `mail.activity.mixin` pour disposer du chatter, du suivi et des activités.

Workflow :

`Brouillon → Soumise → Approuvée → Devis créé → Confirmée → Terminée`

Une réservation peut être annulée avant l'état terminé. L'approbation est réservée au groupe `Responsable Agence de Voyages`.

Intégration standard :

- le client est un contact Odoo (`res.partner`) ;
- le devis est un `sale.order` standard ;
- la facture est gérée par les modules standards Ventes et Facturation/Comptabilité.

### Voyageur

Le modèle `travel.passenger` stocke les voyageurs d'une réservation : nom, date de naissance, âge calculé, nationalité, passeport, téléphone, email et notes.

Règle principale : l'email est contrôlé avec une validation légère pour éviter les formats manifestement incorrects.

## Relations

| Source | Relation | Cible | Cardinalité |
| --- | --- | --- | --- |
| `travel.destination` | contient | `travel.package` | 1-n |
| `travel.package` | planifie | `travel.departure` | 1-n |
| `travel.departure` | reçoit | `travel.booking` | 1-n |
| `travel.booking` | contient | `travel.passenger` | 1-n |
| `res.partner` | client de | `travel.booking` | 1-n |
| `travel.booking` | génère | `sale.order` | 0-1 |
| `res.partner` | fournisseur de | `travel.package` | n-n |

## Sécurité des données

Deux groupes sont définis :

- `Utilisateur Agence de Voyages` : consultation des voyages, création et modification de ses propres réservations et voyageurs ;
- `Responsable Agence de Voyages` : accès complet aux modèles métier, reporting et approbation.

Les règles d'enregistrement limitent les utilisateurs à leurs propres réservations. Les responsables voient toutes les réservations et tous les voyageurs.
