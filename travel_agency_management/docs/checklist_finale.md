# Checklist Finale de Validation

## Exigences générales

| Point | Statut |
| --- | --- |
| Le cahier des charges est traité comme instructions générales | PASS |
| Le sujet réel est “Gestion d’une agence de voyages” | PASS |
| Le projet n'est pas générique | PASS |
| Le projet est centré sur Atlas Horizon Travel, agence de voyages fictive | PASS |
| L'analyse initiale du cahier des charges est documentée | PASS |

## BPMN

| Point | Statut |
| --- | --- |
| Deux processus BPMN sont documentés | PASS |
| Les fichiers BPMN existent | PASS |
| Les fichiers Mermaid existent | PASS |
| Les processus incluent des acteurs/swimlanes | PASS |
| Les étapes automatisées et les étapes Odoo standard sont identifiées | PASS |

## Module Odoo

| Point | Statut |
| --- | --- |
| Le module `travel_agency_management` existe | PASS |
| Le manifeste est présent et syntaxiquement valide | PASS |
| Tous les fichiers Python sont importés | PASS |
| Tous les fichiers XML nécessaires sont référencés | PASS |
| Les fichiers de sécurité sont chargés avant les données et vues | PASS |
| Installation réelle Odoo | FAIL : le lanceur local échoue avec `ModuleNotFoundError: No module named 'odoo'` |
| Mise à jour réelle Odoo | FAIL : même blocage Odoo local |

## Fonctionnel

| Point | Statut |
| --- | --- |
| Gestion des destinations | PASS |
| Gestion des packages | PASS |
| Gestion des départs | PASS |
| Gestion des réservations | PASS |
| Gestion des voyageurs | PASS |
| Workflow de réservation | PASS |
| Contrôle de capacité | PASS |
| Création de devis Odoo | PASS |
| Facturation standard documentée | PASS |
| Bon QWeb PDF | PASS |
| Reporting graph/pivot | PASS |

## Sécurité

| Point | Statut |
| --- | --- |
| Groupe utilisateur | PASS |
| Groupe responsable | PASS |
| Droits d'accès CSV | PASS |
| Règles d'enregistrement | PASS |
| Utilisateurs limités à leurs réservations | PASS |
| Responsables avec accès global | PASS |
| Approbation réservée aux responsables | PASS |

## Interface

| Point | Statut |
| --- | --- |
| Menu principal | PASS |
| Sous-menus | PASS |
| Vues formulaire | PASS |
| Vues liste | PASS |
| Vues recherche | PASS |
| Vues kanban | PASS |
| Vue graph | PASS |
| Vue pivot | PASS |

## Documentation

| Point | Statut |
| --- | --- |
| Rapport projet | PASS |
| Manuel utilisateur | PASS |
| Modèle de données | PASS |
| Cahier de recette | PASS |
| README | PASS |
| Structure académique du rapport | PASS |
| Références aux captures | PASS |

## Captures d'écran

| Point | Statut |
| --- | --- |
| Dossier `docs/screenshots` | PASS |
| Script Playwright | PASS |
| Checklist captures | PASS |
| Captures réelles | FAIL : environnement Odoo local non fonctionnel |
| Images factices | PASS : aucune image factice créée |

## Tests et validations locales

| Point | Statut |
| --- | --- |
| `python3 -m compileall travel_agency_management` | PASS |
| Parsing XML/BPMN Python | PASS |
| `xmllint --noout` XML/BPMN | PASS |
| Vérification des fichiers du manifeste | PASS |
| Tests Odoo réels | FAIL : environnement Odoo local non fonctionnel |
