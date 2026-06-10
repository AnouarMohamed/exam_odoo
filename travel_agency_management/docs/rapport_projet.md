# Rapport de Projet
# Conception et Implémentation d’un SI sous Odoo 17
# Sujet : Gestion d’une agence de voyages

## 1. Introduction

Atlas Horizon Travel est une agence de voyages fictive spécialisée dans la vente de circuits organisés, de séjours touristiques et de départs programmés vers des destinations nationales et internationales. L'agence commercialise des packages comprenant des prestations d'hébergement, de transport, d'assistance et de visites, en relation avec plusieurs prestataires touristiques.

Le secteur d'activité du voyage nécessite une coordination précise entre l'offre commerciale, la disponibilité des départs, la capacité des places, les informations des voyageurs, la relation client, la facturation et la production de documents de voyage. Sans système d'information centralisé, les agents peuvent rencontrer des problèmes de doublons, de manque de visibilité sur les places disponibles, de suivi incomplet des réservations et de difficulté à produire rapidement les bons de réservation.

La problématique retenue est donc la suivante : comment concevoir et développer sous Odoo 17 un système d'information permettant à Atlas Horizon Travel de gérer ses destinations, packages, départs, réservations, voyageurs, devis, factures et documents de réservation dans un workflow fiable et contrôlé ?

Les objectifs du SI sont :

- centraliser les destinations et packages vendus par l'agence ;
- planifier les départs avec une capacité contrôlée ;
- suivre les réservations depuis le brouillon jusqu'à la confirmation ;
- empêcher le surbooking ;
- intégrer les devis et la facturation avec les modules standards Odoo ;
- fournir un reporting graph/pivot ;
- produire un bon de réservation PDF ;
- sécuriser les accès selon les rôles agent et responsable.

Odoo 17 est retenu car il propose une base ERP modulaire, un ORM robuste, des vues métier configurables, un moteur de workflow applicatif, une intégration native avec Contacts, Ventes et Facturation/Comptabilité, ainsi qu'un système de sécurité par groupes et règles d'enregistrement. Ces caractéristiques permettent de construire un module spécifique tout en réutilisant les fonctions standards de l'ERP.

## 2. Modélisation Métier BPMN

Deux processus BPMN sont fournis dans le dossier `docs/bpmn/` et leurs équivalents Mermaid sont fournis dans `docs/diagrams/`.

### Processus 1 : Processus de réservation d’un voyage

Fichiers :

- `docs/bpmn/processus_reservation.bpmn`
- `docs/diagrams/processus_reservation.mmd`

Ce processus décrit le parcours complet depuis la demande initiale du client jusqu'à la génération du bon de réservation. Les acteurs sont le client, l'agent de voyages, le responsable agence et le SI Odoo.

Le client demande une offre. L'agent consulte les destinations, packages et départs disponibles, puis propose une offre. Si le client refuse, le processus se termine. Si le client accepte, l'agent crée une réservation dans Odoo. Le SI vérifie les données obligatoires, l'agent soumet la réservation, puis le responsable vérifie la disponibilité. Une passerelle contrôle les places disponibles. Si la capacité est insuffisante, l'agent propose un autre départ. Si la capacité est suffisante, le responsable approuve la réservation. Odoo crée ensuite le devis via le module Ventes. Après confirmation du client, la facturation est gérée par les modules standards Odoo, puis la réservation est confirmée et le bon PDF est imprimé.

Les étapes automatisées par le module spécifique sont la création de réservation, le workflow, le contrôle de capacité, le lien avec le devis et la génération du bon de réservation. Les étapes gérées par Odoo standard sont la gestion des contacts, le devis de vente et la facturation/comptabilité.

### Processus 2 : Processus de préparation et achat des prestations touristiques

Fichiers :

- `docs/bpmn/processus_prestations.bpmn`
- `docs/diagrams/processus_prestations.mmd`

Ce processus décrit la préparation de l'offre touristique. Le responsable identifie une destination, l'agent crée la destination dans Odoo, puis crée un package avec les services inclus. Le responsable sélectionne les prestataires, les fournisseurs confirment la disponibilité des services, puis une passerelle vérifie si les prestations sont disponibles. Si elles ne le sont pas, le responsable sélectionne un autre prestataire. Si elles le sont, l'agent crée un départ programmé, Odoo suit la capacité, et le responsable ouvre le départ aux réservations.

Le module spécifique couvre la destination, le package, l'association des fournisseurs, le départ et la capacité. Les contacts fournisseurs sont gérés avec le module Contacts. Le processus d'achat détaillé n'a pas été implémenté dans cette version, mais les prestataires sont modélisés par des partenaires fournisseurs afin de préparer une future intégration avec le module Achats.

## 3. Conception du Système d’Information

### Architecture fonctionnelle

Le système est construit autour d'un module spécifique nommé `travel_agency_management`. Ce module s'appuie sur plusieurs modules standards Odoo :

- Contacts : gestion des clients et prestataires ;
- Ventes : création de devis et commandes de vente ;
- Facturation/Comptabilité : génération des factures à partir des commandes confirmées ;
- Messagerie Odoo : suivi des réservations par chatter et activités.

### Modules standards utilisés

Le module Contacts permet d'éviter une base client séparée. Les clients, fournisseurs hôteliers, transporteurs et prestataires touristiques sont des partenaires Odoo. Cette approche garantit une cohérence avec les devis, factures et communications.

Le module Ventes est utilisé pour générer un devis à partir d'une réservation approuvée. La ligne de devis contient le package, la destination, la date de départ et le nombre de voyageurs. Le produit de service utilisé est “Voyage organisé”.

Le module Facturation/Comptabilité n'est pas réinventé. Une fois le devis confirmé, les factures sont produites avec le fonctionnement standard d'Odoo. Cette décision réduit le risque fonctionnel et respecte la logique ERP.

### Module spécifique `travel_agency_management`

Le module spécifique couvre les entités suivantes :

- `travel.destination` : destination touristique ;
- `travel.package` : package vendu par l'agence ;
- `travel.departure` : départ planifié avec capacité ;
- `travel.booking` : réservation et workflow ;
- `travel.passenger` : voyageurs liés à une réservation.

### Modèle de données

Une destination possède plusieurs packages. Un package possède plusieurs départs. Un départ reçoit plusieurs réservations. Une réservation contient plusieurs voyageurs et peut générer un devis Odoo. Les packages peuvent être liés à plusieurs prestataires, qui sont des contacts Odoo fournisseurs.

Le modèle détaillé est documenté dans `docs/modele_donnees.md` et représenté dans `docs/diagrams/modele_donnees.mmd`.

### Rôles et droits d’accès

Deux groupes sont créés :

- Utilisateur Agence de Voyages : peut consulter les destinations, packages et départs, créer et gérer ses propres réservations et voyageurs ;
- Responsable Agence de Voyages : dispose d'un accès complet et peut approuver les réservations.

Les règles d'enregistrement limitent les agents à leurs propres réservations. Les responsables ont accès à toutes les réservations et à tous les voyageurs.

## 4. Réalisation sous Odoo 17

### Structure technique du module

Le module contient les dossiers standards Odoo : `models`, `security`, `data`, `views`, `reports`, `tests` et `docs`. Le fichier `__manifest__.py` déclare les dépendances `base`, `mail`, `contacts`, `sale_management` et `account`.

### Modèles Python

Les modèles Python utilisent l'ORM Odoo, les champs calculés `@api.depends`, les contraintes `@api.constrains`, les exceptions `UserError`, `ValidationError` et `AccessError`, ainsi que le suivi chatter sur les champs importants de la réservation.

Les contrôles principaux sont :

- interdiction des destinations dupliquées par ville et pays ;
- durée de package positive ;
- prix non négatif ;
- capacité de départ positive ;
- dates cohérentes ;
- soumission uniquement avec client, package, départ et voyageurs ;
- approbation uniquement par responsable ;
- blocage du surbooking ;
- interdiction du devis en double ;
- confirmation impossible sans devis.

### Vues XML

Les vues sont rédigées en français et couvrent les listes, formulaires, recherches, kanban, graph et pivot. La réservation dispose d'un formulaire avec statusbar, boutons de workflow et pages :

- Informations générales ;
- Voyageurs ;
- Vente et facturation ;
- Notes ;
- Suivi.

### Workflow

Le workflow principal est :

`Brouillon → Soumise → Approuvée → Devis créé → Confirmée → Terminée`

Les réservations annulées ne consomment pas de capacité. Les réservations brouillon et soumises ne bloquent pas les places. Les places sont consommées seulement à partir de l'état approuvé.

### Rapport QWeb PDF

Le rapport `Bon de réservation` est imprimable depuis `travel.booking`. Il contient :

- Atlas Horizon Travel ;
- référence de réservation ;
- client et contact ;
- date de réservation ;
- package et destination ;
- dates de départ et de retour ;
- nombre de voyageurs ;
- liste des voyageurs ;
- prix unitaire, remise et total ;
- statut ;
- référence du devis si disponible ;
- notes et conditions.

### Vues graph/pivot

Le menu Reporting > Analyse des réservations ouvre une vue graph et une vue pivot. Les analyses permettent de visualiser les réservations par destination, package, statut et mois, avec les mesures `Nombre de voyageurs` et `Montant total`.

### Sécurité

Les fichiers `security.xml`, `ir.model.access.csv` et `record_rules.xml` définissent les groupes, droits d'accès et règles d'enregistrement. Les responsables héritent des droits utilisateurs et disposent d'un accès complet aux modèles métier.

### Intégration avec Ventes/Facturation

Le bouton “Créer le devis” crée un `sale.order` standard. La facturation est ensuite réalisée par Odoo standard à partir de la commande de vente. Le module ne duplique pas les mécanismes comptables.

## 5. Manuel Utilisateur

Les captures doivent être générées dans `docs/screenshots/` avec `scripts/take_screenshots.py` lorsque l'environnement Odoo 17 est disponible. Les références attendues sont :

| Écran | Fichier |
| --- | --- |
| Menu principal | `docs/screenshots/01_menu_principal.png` |
| Liste des destinations | `docs/screenshots/02_liste_destinations.png` |
| Formulaire destination | `docs/screenshots/03_formulaire_destination.png` |
| Liste des packages | `docs/screenshots/04_liste_packages.png` |
| Formulaire package | `docs/screenshots/05_formulaire_package.png` |
| Liste des départs | `docs/screenshots/06_liste_departs.png` |
| Formulaire départ | `docs/screenshots/07_formulaire_depart.png` |
| Liste des réservations | `docs/screenshots/08_liste_reservations.png` |
| Réservation brouillon | `docs/screenshots/09_reservation_brouillon.png` |
| Réservation soumise | `docs/screenshots/10_reservation_soumise.png` |
| Réservation approuvée | `docs/screenshots/11_reservation_approuvee.png` |
| Devis créé | `docs/screenshots/12_devis_odoo.png` |
| Réservation confirmée | `docs/screenshots/13_reservation_confirmee.png` |
| Bon de réservation PDF | `docs/screenshots/14_bon_reservation_pdf.png` |
| Vue graph | `docs/screenshots/15_vue_graph_reservations.png` |
| Vue pivot | `docs/screenshots/16_vue_pivot_reservations.png` |
| Groupes de sécurité | `docs/screenshots/17_groupes_securite.png` |

Le manuel détaillé est disponible dans `docs/manuel_utilisateur.md`.

## 6. Cahier de Recette

Le cahier de recette complet est disponible dans `docs/cahier_recette.md`.

| ID | Scénario | Étapes | Résultat attendu | Statut |
| --- | --- | --- | --- | --- |
| T01 | Créer une destination | Créer pays, ville, nom | Destination enregistrée | À exécuter |
| T02 | Contrôler doublon destination | Créer même ville/pays deux fois | Erreur de validation | À exécuter |
| T03 | Créer un package | Saisir destination, durée, prix | Package brouillon créé | À exécuter |
| T04 | Publier un package | Cliquer Publier | Statut Publié | À exécuter |
| T05 | Ouvrir un départ | Créer départ puis Ouvrir | Départ ouvert | À exécuter |
| T06 | Créer une réservation | Ajouter client, départ, voyageurs | Total et voyageurs calculés | À exécuter |
| T07 | Soumettre | Cliquer Soumettre | Statut Soumise | À exécuter |
| T08 | Approuver | Responsable clique Approuver | Statut Approuvée | À exécuter |
| T09 | Tester surbooking | Dépasser capacité puis approuver | Erreur de capacité | À exécuter |
| T10 | Créer devis | Cliquer Créer le devis | Devis Odoo créé | À exécuter |
| T11 | Confirmer | Cliquer Confirmer la réservation | Réservation confirmée | À exécuter |
| T12 | Imprimer PDF | Cliquer Imprimer le bon | Bon PDF généré | À exécuter |

## 7. Conclusion

Le projet met en place un système d'information Odoo 17 cohérent pour une agence de voyages. Il couvre les besoins essentiels d'Atlas Horizon Travel : gestion de l'offre, planification des départs, réservation, voyageurs, contrôle des places, devis, reporting, sécurité et document PDF.

Les principales difficultés concernent l'alignement entre logique métier spécifique et modules standards Odoo. Le choix retenu consiste à développer uniquement les objets propres au métier du voyage et à réutiliser Odoo pour les contacts, les ventes et la facturation. Cette approche limite les doublons fonctionnels et facilite la maintenance.

Les perspectives d'évolution sont :

- portail client ;
- réservation en ligne ;
- paiement en ligne ;
- intégration CRM ;
- notifications email/SMS ;
- gestion avancée des fournisseurs ;
- tableau de bord avancé ;
- intégration future avec le module Achats.
