# Cahier de Recette

## Objectif

Ce cahier de recette vérifie que le système d'information Odoo 17 développé pour Atlas Horizon Travel couvre le processus de gestion d'une agence de voyages : destinations, packages, départs, réservations, voyageurs, devis, capacité, sécurité, reporting et bon PDF.

## Scénarios de test

| ID | Scénario | Étapes | Résultat attendu | Statut |
| --- | --- | --- | --- | --- |
| T01 | Créer une destination | Ouvrir Agence de Voyages > Voyages > Destinations, créer une destination avec pays et ville. | La destination est enregistrée et visible dans la liste. | À exécuter |
| T02 | Bloquer une destination dupliquée | Créer deux destinations avec la même ville et le même pays. | Odoo affiche une erreur de validation. | À exécuter |
| T03 | Créer un package | Créer un package avec destination, durée, prix et services inclus. | Le package est enregistré en brouillon. | À exécuter |
| T04 | Publier un package | Cliquer sur Publier depuis la fiche package. | Le statut devient Publié. | À exécuter |
| T05 | Créer et ouvrir un départ | Créer un départ pour un package publié puis cliquer sur Ouvrir. | Le départ passe à l'état Ouvert et affiche la capacité. | À exécuter |
| T06 | Créer une réservation brouillon | Créer une réservation avec client, package, départ et voyageurs. | La réservation est en brouillon avec nombre de voyageurs et total calculés. | À exécuter |
| T07 | Soumettre une réservation | Cliquer sur Soumettre. | La réservation passe à Soumise si toutes les données obligatoires sont présentes. | À exécuter |
| T08 | Approuver une réservation | Avec un responsable, cliquer sur Approuver. | La réservation passe à Approuvée si les places sont disponibles. | À exécuter |
| T09 | Refuser le surbooking | Créer une réservation dont le nombre de voyageurs dépasse les places disponibles puis approuver. | Odoo bloque l'approbation avec un message d'erreur. | À exécuter |
| T10 | Créer le devis | Depuis une réservation approuvée, cliquer sur Créer le devis. | Un devis Odoo est créé avec une ligne “Voyage organisé”. | À exécuter |
| T11 | Confirmer la réservation | Cliquer sur Confirmer la réservation après création du devis. | Le devis est confirmé et la réservation passe à Confirmée. | À exécuter |
| T12 | Imprimer le bon | Cliquer sur Imprimer le bon. | Le PDF “Bon de réservation” contient client, voyage, voyageurs, montants et conditions. | À exécuter |
| T13 | Vérifier le reporting | Ouvrir Reporting > Analyse des réservations. | Les vues graph et pivot affichent les montants et voyageurs par destination/package/statut. | À exécuter |
| T14 | Vérifier les droits agent | Se connecter avec un utilisateur agence simple. | L'utilisateur voit ses réservations et ne peut pas approuver. | À exécuter |
| T15 | Vérifier les droits responsable | Se connecter avec un responsable agence. | Le responsable voit toutes les réservations et peut approuver. | À exécuter |

## Tests automatisés

Le fichier `tests/test_travel_workflow.py` couvre les points suivants :

- création d'une destination ;
- création et publication d'un package ;
- création et ouverture d'un départ ;
- création d'une réservation avec voyageur ;
- soumission ;
- approbation ;
- création du devis ;
- confirmation ;
- calcul de capacité ;
- blocage du surbooking.

Ces tests doivent être exécutés dans un environnement Odoo 17 avec le module installé.
