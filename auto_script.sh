#!/usr/bin/bash

REF=$1
INPUT=$2
OUTPUT=$3

print_error () {
    echo "Error: $1"
    echo "Try ./autoscript -h"
}

is_file_valid () {
    if [[ ! -f $1 || $1 != *$2 ]]; then
        print_error "$1 invalid input file path or extension"
        exit 2
    fi
}


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
    echo "      output : output directory, will default to \"out\""
    exit 0
fi

if [ -z $REF ]; then
    print_error "missing argument : reference_file"
    exit 2
elif [ -z $INPUT ]; then
    print_error "missing argument : input"
    exit 2
fi

is_file_valid $REF ".csv"
is_file_valid $INPUT ".zip"

if [ -z $OUTPUT ]; then
    OUTPUT="out_bash"
    # OUTPUT="/media/bigpart/data/CDR/files/CRD-Client"
fi

./vop2pdf.py $REF $INPUT -o $OUTPUT
./vop2csv.py $REF $INPUT -o $OUTPUT
