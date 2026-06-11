# Atlas Horizon Travel - Système d'Information Odoo 17

![Odoo Version](https://img.shields.io/badge/Odoo-17.0-714B67?logo=odoo)
![License](https://img.shields.io/badge/License-LGPL--3-blue)

Ce dépôt contient le projet final de conception de système d'information (SI) réalisé sur **Odoo 17**. Le projet porte sur la gestion complète d'une agence de voyages fictive nommée **Atlas Horizon Travel**.

##  Vue d'ensemble du Projet

L'objectif est de fournir une solution intégrée pour gérer le cycle de vie des produits touristiques, de la conception des packages à la facturation finale des clients, en passant par la gestion des départs et des réservations.

### Fonctionnalités Clés
- **Gestion du Catalogue :** Destinations touristiques et packages de voyage (circuits, séjours).
- **Planification :** Gestion des départs avec suivi de la capacité et des places disponibles.
- **Workflow de Réservation :** Cycle complet de validation (Brouillon → Soumis → Approuvé → Confirmé).
- **Intégration Ventes :** Génération automatique de devis Odoo standard depuis une réservation.
- **Reporting :** Analyses via vues Graph et Pivot, et édition de bons de réservation en PDF (QWeb).
- **Sécurité :** Droits d'accès différenciés pour les Agents et les Responsables.

##  Structure du Dépôt

```text
.
├── module_odoo/               # Code source du module Odoo personnalisé
│   └── travel_agency_management/
│       ├── models/            # Logique métier (Python)
│       ├── views/             # Interfaces (XML)
│       ├── security/          # Droits d'accès et règles
│       ├── reports/           # Modèles de rapports PDF (QWeb)
│       ├── data/              # Données de démonstration et séquences
│       └── tests/             # Tests automatisés
├── bpmn/                      # Modélisation des processus métiers
│   ├── processus_reservation.bpmn
│   └── processus_prestations.bpmn
├── captures_ecran/            # Documentation visuelle (Interface Odoo)
├── rapport_projet_final.pdf   # Rapport de conception complet
└── README.md                  # Ce fichier
```

##  Installation et Utilisation

### Prérequis
- Une instance **Odoo 17** fonctionnelle (Docker ou installation locale).
- Dépendances Odoo : `sale_management`, `account`, `contacts`, `mail`.

### Étapes
1. Clonez ce dépôt ou téléchargez le ZIP.
2. Ajoutez le dossier `module_odoo/travel_agency_management` à votre chemin d'addons Odoo (`addons_path`).
3. Redémarrez votre serveur Odoo.
4. Activez le **mode développeur** dans Odoo.
5. Allez dans **Applications > Mise à jour de la liste des applications**.
6. Recherchez "Gestion d’une agence de voyages" et cliquez sur **Installer**.

##  Tests
Le module inclut des tests automatisés couvrant le workflow nominal et les contrôles de capacité.
Pour lancer les tests :
```bash
odoo-bin -d <votre_base> -i travel_agency_management --test-enable --stop-after-init
```

##  Documentation Complète
Pour plus de détails sur la conception technique, les choix d'architecture et le manuel utilisateur, veuillez consulter le fichier [rapport_projet_final.pdf](./rapport_projet_final.pdf) présent à la racine.

---
**Auteur :** Anouar Mohamed  
**Projet :** Examen Final - Conception de SI (Odoo 17)
