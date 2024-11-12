#!/usr/bin/bash

PROJ_LOC="/usr/Vop2x/"
REF_FILE=$1
OUT_FOLD=$2
ZIP_FILE=$(date --date='-1 month' +"%Y-%m.zip" | tr -d '\n')
ZIP_FOLD="$PROJ_LOC/zip/"
PASS=""
USER=""
IP=""

print_error () {
    echo "Error: $1"
    echo "Try ./autoscript -h"
}

is_file_valid () {
    if [[ ! -f $1 || $1 != *$2 ]]; then
        print_error "$1 invalid input file path or extension"
        retun 2
    fi
}

# Help
if [ "$1" == "-h" ]; then
    echo "Usage:"
    echo "      automakefile reference input [output]"
    echo
    echo "Description:"
    echo "      Executes vop2x programs with given directions\n"
    echo
    echo "      reference : client mobile data csv file"
    echo "          ex : data_repertoire/Base_de_donnees_mobiles_data.csv\n"
    echo
    echo "      input : zip file extracted from VOP containing data to be treated"
    echo "          ex : zip/2024-03.zip"
    echo
    echo "      output : output directory, will default to \"/media/bigpart/data/CDR/files/CRD-Client\""
    exit 0
fi

# Error handling
if [ -z $REF_FILE ]; then
    print_error "missing argument : reference_file"
    exit 2
elif [ -z $ZIP_FOLD ]; then
    print_error "missing argument : input"
    exit 2
fi

is_file_valid $REF_FILE ".csv"

# Récupère le zip via un protocole ftp, peut être rendu plus sécurisé
wget "ftp://${USER}:${PASS}@${IP}/$ZIP_FILE" -P $ZIP_FOLD

# Fichier output pour clients, définissable pour débug
if [ -z $OUT_FOLD ]; then
    OUT_FOLD="/media/bigpart/data/CDR/files/CRD-Client"
fi

# Commandes Vop2x (adaptables)
$PROJ_LOC/vop2pdf.py $REF_FILE $ZIP_FOLD$ZIP_FILE -d -o $OUT_FOLD
$PROJ_LOC/vop2csv.py $REF_FILE $ZIP_FOLD$ZIP_FILE -d -o $OUT_FOLD

