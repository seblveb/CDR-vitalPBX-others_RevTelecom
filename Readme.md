# Vop2X

Outil de conversion d'export de vop

Ce dépot contient :

1. [VOP2PDF](#vop2pdf) : Créé un graph de la consommation de data trié par client puis par date
2. [VOP2CSV](#vop2csv) : Crée un csv par client regroupant la consommation de forfait mobile par mois et par puce
3. [AUTO_SCRIPT](#auto_script) : éxécute les deux programmes avec les arguments prodigués

## Sommaire

- [Vop2X](#vop2x)
  - [Sommaire](#sommaire)
  - [Prérequis](#prérequis)
  - [VOP2PDF](#vop2pdf)
      - [- Utilisation](#--utilisation)
      - [Description](#description)
  - [VOP2CSV](#vop2csv)
      - [- Utilisation](#--utilisation-1)
      - [- Description](#--description)
  - [auto\_script](#auto_script)
      - [- Utilisation](#--utilisation-2)
      - [- Description](#--description-1)

## Prérequis

1. Un fichier de référence, base de données contenant tous les numéros à traiter (ex: Base_de_donnees_mobiles_data.csv)
2. Un fichier zip des cdr exporté directement de VOP (ex: 2024-01.zip)
3. (optionnel) Un dossier ou exporter
4. (autoscript) Des crédentiels de connection en ftp pour récupérer les fichiers d'exports

## VOP2PDF

#### - Utilisation

```sh
$ ./vop2pdf ref zip -o output
# voir arguments dans prérequis
```
#### Description

Analyse les fichiers DATA et génère, répartis en dossier clients et sous dossier date :
- Un graphique représentant la consommation sur le mois
- Un tableau CSV comprennant les données utilisées dans le traitement du graph

## VOP2CSV

#### - Utilisation

```sh
$ ./vop2pdf ref zip -o output
# voir arguments dans prérequis
```
#### - Description

Analyse tous les fichiers et génère, pour chaque client, un fichier regroupant les Hors-Forfaits de toutes les puces ayant dépassées leur forfait durant le mois.

## auto_script

#### - Utilisation

```
$ ./auto_script ref zip_dir [output]
# voir arguments dans prérequis
```

#### - Description

Execute les deux programmes avec les arguments prodigués

zip_dir correspond au dossier contenant les fichiers zip à extraire, le zip sera déterminé automatiquement en fonction de la date (date d'un mois avant l'execution)

Si pas d'output précisée, l'output par défaut est utilisée ("out" ou autre dossier au cas par cas)
