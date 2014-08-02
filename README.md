zaphir
======

**La branche master de Zaphir correspond à la version 1.07.**
**La branche 1.08 de Zaphir est la branche de développement.**

# Zaphir

Cette application permet de générer un fichier de métadonnées au format d'échange XML conforme à la directive européenne INSPIRE et aux recommandations nationales, à partir d'un fichier Excel "Elexire" (cf. "un fichier Excel pour décrire vos données géographiques").

## Notes de version:
Pour plus d'information sur l'historique des versions et son évolution, cf. fichier history.txt.
  - La vesion 1.0 de Zaphir fonctionne avec la version 1.18 du fichier Elexire.
  - La vesion 1.01 de Zaphir fonctionne avec la version 1.18 du fichier Elexire.
  - La vesion 1.04 de Zaphir fonctionne avec la version 1.21 du fichier Elexire.
  - La vesion 1.05 de Zaphir fonctionne avec la version 1.22 du fichier Excel.
  - La vesion 1.06 de Zaphir fonctionne avec la version 1.22 du fichier Excel pour la description des données et la version 0.01 du fichier Excel pour la description des cartes.
  - La vesion 1.07 de Zaphir fonctionne avec la version 1.23 du fichier Excel pour la description des données et la version 0.01 du fichier Excel pour la description des cartes.

## Limites et erreurs connues:
  - Zaphir 1.06 : des messages d'erreur indiquant l'absence de champs obligatoires peuvent appraître dans le fichier d'erreur, notamment lors du traitement de fichiers de description de cartes.
  - Zaphir 1.07 : des messages d'erreur indiquant l'absence de champs obligatoires peuvent appraître dans le fichier d'erreur, notamment lors du traitement de fichiers de description de cartes.

## Usage simple:
Après téléchargement de l'application et décompression de l'archive, lancer l'application par double-clic sur le fichier "zaphir.exe".

  - Sélectionnez un dossier contenant des fichiers Elexire au format Excel (XLS) adaptés à la saisie des métadonnées selon la norme ISO 19115.
  - Sélectionnez un dossier de destination et/ou contenant une liste de fichiers au format XML (ISO 19139).
  - Choisissez l'action à réaliser:

  - Le bouton "Quitter" permet de quitter l'application.
  - Le bouton "Actualiser les listes" permet simplement de relire le contenu des dossiers sélectionnés et recharger la liste des fichiers.
  - Le bouton "XLS vers XML" permet de convertir un fichier XLS sélectionné au format XML conforme ISO19139/INSPIRE.
  - Le bouton "Voir fiche" permet de consulter la fiche XML sélectionnée avec une mise en page html.

## Développement:
Cette application a été développée dans le cadre du groupe de travail CIGAL sur les métadonnées.
Pour tout renseignement, contactez: guillaume.ryckelynck(at)region-alsace.eu

## Todo:
  - Adapter les messages d'erreur en fonction du fichier Excel présenté. Si representationType = map, c'est une fiche de description de carte.
  - Mettre à jour le fichier Excel présent dans le dépôt.
  - Ajouter le fichier Excel de carte dans le dépot.
  - Nettoyer le code.
  - Mettre à jour la documentation.

## Licence:
Cette application peut-être librement réutilisée et adaptée, dans la mesure où les sources sont citées.
G. Ryckelynck - Partenariat CIGAL 2011-2014 (www.cigalsace.org)
