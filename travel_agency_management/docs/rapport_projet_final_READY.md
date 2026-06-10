## 1. Introduction

Ce rapport présente les travaux de conception et de réalisation d'un système d'information (SI) sous Odoo 17 pour la gestion d'une agence de voyages. L'activité de cette agence repose sur l'organisation et la commercialisation de séjours touristiques structurés sous forme de packages avec des départs programmés.

### Présentation de l'agence

L'agence de voyages commercialise des offres de séjours et des circuits packagés. Ces prestations associent le transport, l'hébergement et des activités de loisirs. Chaque package est ensuite planifié à des dates précises avec des contraintes physiques de capacité.

### Problématique métier

L'organisation des départs nécessite le suivi rigoureux de plusieurs contraintes opérationnelles :

* **Calcul de capacité et surbooking** : Chaque départ de voyage possède un nombre de places limité. L'absence de contrôle dynamique peut entraîner une vente excédentaire par rapport aux places de transport ou d'hébergement disponibles.

* **Double saisie des données** : Le manque d'intégration logicielle oblige les agents à ressaisir manuellement les informations des voyageurs (noms, dates de naissance, numéros de passeport) lors des phases de facturation et d'impression des bons de voyage.

* **Traçabilité des dossiers** : Il est nécessaire de suivre précisément l'avancement de chaque réservation, de sa création à la facturation comptable finale.

### Objectifs du système d'information

Le système d'information mis en place doit répondre aux objectifs suivants :

* Centraliser le catalogue des destinations géographiques et des packages.

* Automatiser le calcul de la disponibilité en temps réel sur les départs ouverts.

* Bloquer les ventes si le nombre de places demandées excède la capacité résiduelle.

* Intégrer les dossiers de réservation avec le module standard des Ventes d'Odoo.

* Fournir un tableau de bord et des vues analytiques pour suivre la performance commerciale.

* Imprimer le Bon de réservation officiel contenant toutes les données réglementaires des voyageurs.

### Choix technologique d'Odoo 17

Pour implémenter ce système d'information, la plateforme ERP Odoo 17 a été sélectionnée. Elle offre une structure modulaire s'appuyant sur l'ORM Python et une base relationnelle PostgreSQL. Cette architecture permet de développer les objets métiers spécifiques tout en tirant parti des applications comptables et commerciales natives de l'ERP.

---

## 2. Modélisation métier BPMN

La modélisation des processus métiers a été réalisée en respectant la norme BPMN afin de structurer les flux et d'identifier la répartition des tâches entre les développements spécifiques et les fonctions natives d'Odoo.

### 2.1 Processus de réservation d’un voyage

Ce diagramme décrit les actions successives menant de la demande client à la confirmation finale et à la remise du titre de transport.

<!-- DIAGRAM_RESERVATION -->

#### Rôles des acteurs :

* **Le Client** : Exprime son besoin, accepte le tarif proposé, puis valide la commande par son paiement.

* **L'Agent de Voyages** : Gère la saisie des dossiers, ajoute la liste des passagers et transmet la demande au système.

* **Le Responsable Agence** : Exécute le rôle de contrôle en approuvant le dossier après s'être assuré de la disponibilité des places.

* **Le SI Odoo** : Calcule dynamiquement les places, crée le devis standard et génère le fichier PDF du bon de voyage.

#### Alignement des fonctionnalités :

* **Éléments automatisés par le module** : Création de la réservation, validation de la capacité, gestion du workflow et génération du rapport PDF.

* **Éléments gérés par Odoo standard** : Fiche client (Contacts), validation du devis (Ventes), émission de la facture et enregistrement du paiement (Comptabilité).

---

### 2.2 Processus de préparation des prestations touristiques

Ce processus décrit la structuration du catalogue de voyages en amont de la saison de vente.

<!-- DIAGRAM_PRESTATIONS -->

#### Rôles des acteurs :

* **Le Responsable Agence** : Négocie les prestations hôtelières et de transport, valide les accords et ouvre les départs.

* **L'Agent de Voyages** : Enregistre les fiches techniques des destinations et assemble les packages commerciaux.

* **Le Fournisseur** : Valide la disponibilité globale des chambres ou des sièges de transport.

* **Le SI Odoo** : Contraint la cohérence des dates, des tarifs et gère l'inventaire logique de capacité.

#### Alignement des fonctionnalités :

* **Éléments automatisés par le module** : Enregistrement de la destination unique, composition du package et planification du départ réel avec dates contraintes.

* **Éléments gérés par Odoo standard** : Fiches d'identité des prestataires dans Contacts.

---

## 3. Conception du système d’information

La conception du système d'information repose sur l'intégration entre les applications natives d'Odoo et le module développé spécifiquement.

### Modules Odoo standards utilisés

Le système d'information réutilise quatre applications natives de l'ERP :

1. **Contacts (`contacts`)** : Utilisé pour héberger les clients (acheteurs) et les prestataires (fournisseurs hôteliers ou transporteurs) sur la table commune `res.partner`.

2. **Ventes (`sale_management`)** : Utilisé pour matérialiser le devis commercial et la commande via `sale.order`.

3. **Facturation/Comptabilité (`account`)** : Prise en charge standard de l'émission des factures clients et du lettrage des paiements.

4. **Messagerie (`mail`)** : Fournit le chatter collaboratif et le journal des modifications sur la fiche réservation.

### Rôle du module spécifique

Le module personnalisé `travel_agency_management` gère les entités de l'activité voyage, assure la vérification de la capacité des départs à l'approbation et orchestre la passerelle vers la création de devis de vente.

### Diagramme du modèle de données

Le modèle conceptuel relationnel présente les tables créées et leurs interactions avec les objets Odoo.

<!-- DIAGRAM_DATA_MODEL -->

### Description des principales entités

* **Destination (`travel.destination`)** : Ville et pays du voyage. Comporte une contrainte d'unicité logique pour empêcher la création de doublons par ville et pays.

* **Package (`travel.package`)** : Formule vendable combinant une destination, une durée en jours et un tarif de base. Il est lié aux partenaires prestataires.

* **Départ (`travel.departure`)** : Session de voyage planifiée (ex. : départ du 15 juillet). Il définit la date de départ, la date de retour calculée, la capacité en nombre de sièges et calcule les places restantes.

* **Réservation (`travel.booking`)** : Dossier de voyage client. Elle suit les étapes du workflow, calcule le montant total (prix unitaire x voyageurs - remise) et pointe vers le devis généré.

* **Voyageur (`travel.passenger`)** : Fiche individuelle de chaque passager liée à la réservation. Odoo calcule l'âge de chaque passager à partir de sa date de naissance.

### Sécurité et droits d'accès

La sécurité du système d'information est configurée à travers trois fichiers :

* **Groupes d'accès (`security/security.xml`)** :
  * *Utilisateur Agence de Voyages* : Conçu pour les agents commerciaux. Permet la consultation des destinations/packages et la gestion de leurs propres réservations.
  * *Responsable Agence de Voyages* : Permet le paramétrage des départs, la modification des tarifs et détient le droit exclusif d'approuver une réservation.

* **Règles d'enregistrement (`security/record_rules.xml`)** :
  * Un agent ne voit que les réservations qu'il a créées ou dont il est responsable.
  * Le responsable d'agence dispose d'un accès global sans filtre de confidentialité.

* **ACLs (`security/ir.model.access.csv`)** :
  * Définit les droits CRUD par modèle PostgreSQL pour chaque groupe d'utilisateurs.

---

## 4. Réalisation et Manuel Utilisateur

Le module a été développé selon l’architecture habituelle d’un module Odoo : modèles Python, vues XML, règles de sécurité et rapports QWeb.

### 4.1 Réalisation technique sous Odoo 17

#### 4.1.1 Structure du module
Le code source respecte l'arborescence standard d'Odoo :
* `models/` : travel_booking.py, travel_departure.py, travel_destination.py, travel_package.py, travel_passenger.py.
* `views/` : Vues et formulaires XML associés à chaque modèle.
* `security/` : Groupes de sécurité et matrice d'accès CSV.
* `reports/` : Déclaration et gabarit QWeb du Bon de réservation PDF.
* `data/` : Séquence automatique et données de test.

#### 4.1.2 Modèles Python
Les modèles s'appuient sur l'ORM d'Odoo. Des décorateurs Python valident les données :
* `@api.depends` : Recalcule dynamiquement les places disponibles du départ à chaque modification du statut des réservations liées.
* `@api.constrains` : Interdit l'enregistrement si la capacité est inférieure à zéro, si les dates de départ/retour sont incohérentes, ou si une destination dupliquée est saisie.

#### 4.1.3 Vues XML et menus
L'interface utilisateur intègre le menu principal et des sous-menus pour naviguer entre les réservations, les départs et le reporting. Les formulaires intègrent des statusbars interactifs et des feuilles de style pour masquer les boutons d'action selon l'état du dossier.

#### 4.1.4 Workflow
Le cycle de vie d'un dossier réservation comporte sept états :
`Brouillon (draft) -> Soumise (submitted) -> Approuvée (approved) -> Devis créé (sale_created) -> Confirmée (confirmed) -> Terminée (done) / Annulée (cancelled)`
L'ORM bloque le passage à l'état approuvé si le nombre de passagers est supérieur aux sièges restants.

#### 4.1.5 Intégration au devis Odoo
À l'état approuvé, l'agent clique sur le bouton de facturation. Odoo instancie automatiquement un devis dans l'application Ventes standard (`sale.order`) en y insérant une ligne d'article de service « Voyage organisé » valorisée au prix du package multiplié par le nombre de voyageurs.

#### 4.1.6 Rapport QWeb
Le document client « Bon de réservation » est un modèle de rapport QWeb HTML associé à l'action d'impression Odoo. Il compile les données clients, les caractéristiques du voyage, la liste nominative des voyageurs avec leur passeport et les conditions générales de vente.

#### 4.1.7 Reporting graph/pivot
Deux vues de synthèse ont été ajoutées pour suivre les réservations : une vue graphique (histogramme ou camembert) et une vue pivot (tableau croisé dynamique) pour analyser le chiffre d'affaires et les volumes de passagers.

#### 4.1.8 Sécurité
Les règles de record-level security (sécurité à l'enregistrement) filtrent les enregistrements PostgreSQL renvoyés à l'interface graphique selon le profil de l'utilisateur connecté.

---

### 4.2 Manuel Utilisateur avec Captures d'Écran

Cette section présente les étapes de manipulation du module illustrées par les écrans de l'application.

#### 4.2.1 Accès au menu principal
Une fois connecté en tant qu'agent commercial, le menu principal **Agence de Voyages** s'affiche dans l'en-tête.

![Figure 1 - Vue du menu principal et des sous-menus](screenshots/01_menu_principal.png)

#### 4.2.2 Liste des destinations
Le sous-menu `Voyages > Destinations` affiche les villes disponibles pour la création des séjours.

![Figure 2 - Vue en liste des destinations configurées](screenshots/02_liste_destinations.png)

#### 4.2.3 Formulaire de package
Le formulaire package permet de définir les prix, la destination et la durée en jours du voyage.

![Figure 5 - Formulaire d'édition d'un package commercial](screenshots/05_formulaire_package.png)

#### 4.2.4 Liste des départs planifiés
La liste des départs permet de suivre les dates planifiées et de vérifier le nombre de places restantes avant de soumettre une réservation.

![Figure 6 - Vue en liste des départs de voyages planifiés](screenshots/06_liste_departs.png)

#### 4.2.5 Enregistrement d'une réservation (Brouillon)
L'agent commercial crée une réservation en renseignant le client, le package et la liste nominative des voyageurs.

![Figure 9 - Fiche de réservation à l'état Brouillon](screenshots/09_reservation_brouillon.png)

#### 4.2.6 Soumission et Approbation du dossier
Après vérification par l'agent, le dossier est soumis. Le responsable d'agence valide l'approbation, ce qui bloque logiquement les places sur le départ.

![Figure 10 - Fiche de réservation à l'état Soumise](screenshots/10_reservation_soumise.png)

![Figure 11 - Fiche de réservation approuvée par le responsable d'agence](screenshots/11_reservation_approuvee.png)

#### 4.2.7 Génération du devis de vente
À l'approbation, l'agent clique sur la génération de devis. Odoo crée la commande commerciale standard.

![Figure 12 - Devis commercial standard Odoo généré à partir de la réservation](screenshots/12_devis_odoo.png)

#### 4.2.8 Confirmation de réservation
Après paiement du client et confirmation de la vente standard Odoo, la réservation passe à l'état final Confirmée.

![Figure 13 - Fiche de réservation confirmée après confirmation de la vente](screenshots/13_reservation_confirmee.png)

#### 4.2.9 Impression du Bon PDF
L'impression génère le document officiel de transport destiné aux voyageurs.

![Figure 14 - Rendu du document PDF du bon de réservation client](screenshots/14_bon_reservation_pdf.png)

#### 4.2.10 Reporting graphique
La vue graphique permet de suivre le nombre de réservations passées par destination.

![Figure 15 - Vue graphique d'analyse des réservations](screenshots/15_vue_graph_reservations.png)

#### 4.2.11 Reporting pivot
La vue pivot affiche un tableau croisé dynamique pour analyser les montants de vente par package et par mois.

![Figure 16 - Tableau croisé pivot d'analyse des montants](screenshots/16_vue_pivot_reservations.png)

#### 4.2.12 Gestion de la sécurité
L'affectation des groupes utilisateurs (Agent ou Responsable) est configurée dans l'administration d'Odoo.

![Figure 17 - Configuration des droits d'accès utilisateurs sous Odoo 17](screenshots/17_groupes_securite.png)

---

### 4.3 Cahier de Recette / Tests Fonctionnels

Ce tableau synthétise les tests de validation fonctionnelle réalisés sur le module.

| ID | Scénario de test | Étapes de test | Résultat attendu | Résultat obtenu | Statut |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **T01** | Installation du module | Installer `travel_agency_management` sur Odoo 17. | Installation réussie, structure de base créée. | Conforme | **Succès** |
| **T02** | Création d’une destination | Renseigner ville et pays dans le formulaire destination. | Enregistrement correct en base de données. | Conforme | **Succès** |
| **T03** | Test d'unicité destination | Créer deux destinations identiques (même ville et pays). | Odoo refuse la validation et lève une exception. | Blocage OK | **Succès** |
| **T04** | Création de package | Saisir durée et prix puis enregistrer. | Package créé et initialisé à l'état Brouillon. | Conforme | **Succès** |
| **T05** | Valeurs package invalides | Saisir une durée <= 0 ou un tarif négatif. | L'ORM rejette l'écriture avec une boîte de dialogue. | Rejet OK | **Succès** |
| **T06** | Publication de package | Cliquer sur `Publier` sur la fiche package. | Le package passe à l'état `Publié`. | Conforme | **Succès** |
| **T07** | Création de départ | Saisir les dates de départ, la capacité et passer à `Ouvert`. | Le départ est ouvert et suit les réservations. | Conforme | **Succès** |
| **T08** | Saisie de réservation | Choisir le package, le départ et lister des passagers. | Odoo charge le prix et calcule le total. | Conforme | **Succès** |
| **T09** | Âge des voyageurs | Saisir la date de naissance d'un passager. | Calcul dynamique automatique de l'âge. | Conforme | **Succès** |
| **T10** | Soumission réservation | Cliquer sur `Soumettre`. | Le dossier passe à l'état `Soumise`. | Conforme | **Succès** |
| **T11** | Approbation | Cliquer sur `Approuver` (Profil Responsable). | Le dossier passe à `Approuvée`. | Conforme | **Succès** |
| **T12** | Test de surbooking | Créer une réservation excédant la capacité restante et approuver. | Odoo bloque l'action et signale l'erreur de places. | Blocage OK | **Succès** |
| **T13** | Génération du devis | Cliquer sur `Créer le devis` depuis la fiche approuvée. | Un devis `sale.order` lié est généré dans Odoo Ventes. | Devis lié | **Succès** |
| **T14** | Confirmation finale | Confirmer le devis puis cliquer sur `Confirmer la réservation`. | La réservation passe à l'état `Confirmée`. | Conforme | **Succès** |
| **T15** | Édition du PDF | Cliquer sur `Imprimer le bon` sur une réservation validée. | Téléchargement du bon de réservation PDF conforme. | Conforme | **Succès** |

---

## 5. Conclusion

La mise en place du système d'information de l'agence de voyages à travers le module développé sous Odoo 17 démontre l'apport d'un ERP pour unifier des processus métiers spécifiques.

### Bilan opérationnel

L'application répond aux exigences opérationnelles clés :
* Le suivi des disponibilités et le blocage automatique du surbooking fiabilisent la gestion de capacité des départs.
* L'intégration avec l'application de Ventes standard d'Odoo évite la ressaisie manuelle des voyageurs lors des phases comptables et de facturation.
* La gestion de sécurité par groupes garantit le contrôle des opérations sensibles comme la validation des tarifs et l'approbation finale des dossiers.

### Limitations et perspectives

Quelques axes d'amélioration demeurent ouverts pour les versions ultérieures du système :
* **Automatisation complète du cycle d'achat** : Les prestataires de transport ou d'hébergement sont enregistrés dans les contacts, mais le système ne génère pas de demande de prix ou de bon d'achat (`purchase.order`) standard automatique. L'intégration avec le module d'Achats standard constitue la principale perspective d'évolution.
* **Synchronisation comptable** : La confirmation finale de la réservation nécessite une action manuelle après confirmation de la vente. Un déclencheur basé sur le lettrage complet de la facture de vente correspondante permettrait d'automatiser cette transition d'état.
