Cahier des Charges
Projet de Conception de SI sur Odoo 17
1. Contexte et Objectifs
Dans le cadre du cours de conception de SI, les étudiants doivent concevoir et implémenter
un système d'information (SI) sur Odoo17 pour une entreprise fictive attribuée par
l'enseignant. Le projet suit une démarche complète : de la modélisation des processus
métiers jusqu'au développement d’un nouveau module Odoo 17 couplé à l’utilisation de
modules existants.

Objectifs pédagogiques :

Analyser et modéliser les processus métiers d'une organisation à l'aide de la norme
BPMN.
Développer un module personnalisé répondant à un besoin métier spécifique.
Intégrer des modules standards d’Odoo (ex. : Ventes, Achats, Inventaire) pour unifier le
SI.
Appliquer les bonnes pratiques de développement Odoo (MVC, sécurité, vues).
Documenter la démarche de conception et de réalisation à travers un rapport
professionnel.
2. Phase 1 : Modélisation des Processus Métiers (BPMN)
Avant tout développement, les étudiants doivent cartographier les processus clés de leur
sujet. Cette phase doit obligatoirement figurer dans le rapport final.

Identification des processus : Définir au moins deux processus métiers majeurs liés au
sujet (ex: processus de réservation, cycle d'achat/vente, admission d'un patient).
Modélisation BPMN : Réaliser les diagrammes en utilisant les bonnes pratiques de la
norme (Pools, Swimlanes pour les acteurs, événements de début/fin, passerelles
logiques, tâches).
Alignement SI : Le modèle doit clairement identifier quelles étapes seront automatisées
par le module spécifique à développer et quelles étapes seront gérées par les modules
standards d'Odoo.
3. Phase 2 : Spécifications Fonctionnelles et Techniques (Odoo 17)
3.1. Attentes Fonctionnelles

Nouveau module spécifique :
Développement d’un module répondant au cœur de métier du sujet attribué.
Implémentation d’au moins un processus métier clé avec workflow (ex. : validation
d’une commande, changement d'état d'un dossier).
Utilisation de modules existants :
Intégration et configuration de modules standards Odoo pour gérer les fonctions
transverses de l’entreprise.
Interface utilisateur (UI) :
Création de vues formulaires, listes (tree) et kanban pour les nouvelles entités.
Mise en place d'un menu personnalisé pour naviguer dans le module.
Rapports et tableaux de bord :
Création d’au moins un rapport imprimable (QWeb PDF).
Visualisation des données clés (ex. : vue graph ou pivot pour les statistiques).
Sécurité et Droits d'accès :
Gestion des groupes de sécurité (fichiers ir.model.access.csv et règles records).
Séparation des rôles (ex. : simple utilisateur vs manager).
3.2. Contraintes Techniques

Plateforme : Odoo 17 (Environnement de développement via Docker ou installation
locale).
Langages : Python (logique métier/models), XML (vues, menus, rapports), JavaScript
(optionnel pour les fonctionnalités avancées de l'UI).
Structure du code : Respect strict des conventions de l'ORM Odoo (fichiers
manifest.py, architecture MVC via les dossiers models, views, security, reports).
Dépendances : Déclaration correcte des dépendances (modules standards) dans le
manifest.
4. Phase 3 : Livrables et Rédaction du Rapport
À l'issue du projet, les étudiants devront remettre le code source de leur module ainsi qu'un
rapport de projet structuré comme suit :

Introduction : Présentation de l'entreprise fictive, de son secteur d'activité et de la
problématique traitée.
Modélisation Métier (BPMN) : Présentation des diagrammes BPMN et explication
textuelle des flux et des rôles des différents acteurs.
Conception du Système d'Information : Choix des modules standards Odoo retenus et
justification. Modèle de données (Diagramme de classes ou relationnel des entités créées
dans le nouveau module).
Réalisation et Manuel Utilisateur : Démonstration du fonctionnement avec des captures
d'écran (menus, vues, flux de validation, rapports) et mise en évidence de la gestion des
droits d'accès.
Conclusion : Bilan du projet, difficultés rencontrées et perspectives d'évolution du SI.
