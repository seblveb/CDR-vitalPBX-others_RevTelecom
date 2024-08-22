#!/usr/bin/python3

#own
from vop2csv_parse import parse_arguments
from vop2unzip import unzip_file

#native
from collections import defaultdict
from itertools import chain
from pathlib import Path
import csv
import os


def print_debug(string: str):
    if args.debug :
        print("DBG:", string)

# Isole le numéro du téléphone du nom de fichier
get_phone = lambda x : x.split('-')[-1][:-4]


def process_file(number: str, mobile_files: list[str], data_files: list[str], margin: int) -> int:
    mobile_file_list = [n for n in mobile_files if number in n]
    data_file_list = [n for n in data_files if number in n]

    # Récupère la première ligne correspondante du fichier source (Nom, etc..)
    infos = [c for c in source if number in c][0]
    print_debug("client: {}".format(infos))

    to_write = [infos[2], infos[0], infos[3]]

    #{ Peut être transformé en fonction
    if not mobile_file_list:
        print_debug("{} no mobile plan".format(number))
        to_write.append(0.0)
    else :
        with open(mobile_file_list[0]) as file:
            reader =csv.reader(file)
            total = 0
            next(reader)
            for row in reader:
                if ("RG9000.mobiledata" not in row[9]):
                    total += float(row[7])
            mobile_margin = round(total / ((100 - margin) * 0.01), 2)
            to_write.append(mobile_margin)

    #{ Peut être transformé en la même fonction
    if not data_file_list:
        print_debug("{} no data plan".format(number))
        to_write.append(0.0)
    else:
        with open(data_file_list[0]) as file:
            reader =csv.reader(file)
            total = 0
            next(reader)
            for row in reader:
                total += float(row[6])
            data_margin = round(total / ((100 - margin) * 0.01), 2)
            to_write.append(data_margin)

    writing = to_write[3] + to_write[4]

    print(writing)

    if writing != 0 :
        writer.writerow(to_write)

    return writing


if __name__ == '__main__':

    args = parse_arguments()
    source_dico = defaultdict(list)

    # Récupère les numéros du fichier source dans un dictionnaire par clients
    with open(args.source_file) as source_file :
        source_reader = csv.reader(source_file)
        next(source_reader)
        source = [r for r in source_reader]
        for row in source:
            source_dico[row[1]].append(row[0])

    # Dézip le dossier
    dir = unzip_file(args.zip_file)

    # Récupère les fichiers MOBILES & DATA
    mobile_files = [dir + "/" + f for f in os.listdir(dir)
        if "DATA" not in f and get_phone(f) in chain(*source_dico.values())]
    data_files = [dir + "/" + f for f in os.listdir(dir)
        if "DATA" in f and get_phone(f) in chain(*source_dico.values())]

    # Marge à calculer
    margin = int(args.margin) if args.margin else 36

    # Récupère la date via le dossier dézipé
    date = dir.split('/')[-1]
    out_dir = args.output_dir if args.output_dir else "out"

    client: str
    for client in source_dico:

        written = 0

        # Créé le fichier et le dossier parent
        Path("{}/{}".format(out_dir, client)).mkdir(parents=True, exist_ok=True)
        csv_file = "{}/{}/Hors_Forfait_{}_{}.csv".format(out_dir, client,
                        client.replace(' ', '_').replace('.', ''), date)

        # Ouvre fichier >>-->
        output = open(csv_file, 'w+')

        # Créé le writer et
        writer = csv.writer(output)
        writer.writerow(["Client", "Numéro", "Puce", "Total mobile marginé", "Total data marginé"])

        for x in source_dico[client]:
            print_debug("looking at {}".format(x))
            written += process_file(x, mobile_files, data_files, margin)

        # Ferme fichier <--<<
        output.close()

        # Supprime le fichier si aucune puce forfait mobile
        if (written == 0):
            os.remove(csv_file)

