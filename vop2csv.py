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

def process_file(number: str, all_files: list[str], margin: int):
    file_list = [n for n in all_files if number in n]

    if not file_list:
        print_debug("{} no mobile plan".format(number))
        return 0

    infos = [c for c in source if number in c][0]
    print_debug("client: {}".format(infos))

    with open(file_list[0]) as file:
        reader =csv.reader(file)
        total = 0

        next(reader)
        for row in reader:
            total += float(row[7])
        total_margin = round(total / ((100 - margin) * 0.01), 2)

        to_write = [infos[2], infos[0], infos[3], total_margin]
        writer.writerow(to_write)

    return 1


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

    # Récupère les dossiers NON DATA (à changer si identifiables)
    files = [dir + "/" + f for f in os.listdir(dir)
        if "DATA" not in f and get_phone(f) in chain(*source_dico.values())]

    # Marge à calculer
    margin = int(args.margin) if args.margin else 36

    # Récupère la date via le dossier dézipé
    date = dir.split('/')[-1]
    out_dir = args.output_dir if args.output_dir else "out"

    for client in source_dico:

        written = 0

        # Créé le fichier et le dossier parent
        Path("{}/{}".format(out_dir, client)).mkdir(parents=True, exist_ok=True)
        csv_file = "{}/{}/Forfaits_mobiles_{}.csv".format(out_dir, client, date)

        # Ouvre fichier >>-->
        output = open(csv_file, 'w+')

        # Créé le writer et
        writer = csv.writer(output)
        writer.writerow(["Client", "Numéro", "Puce", "Total marginé"])

        for x in source_dico[client]:
            print_debug("looking at {}".format(x))
            written += process_file(x, files, margin)

        # Ferme fichier <--<<
        output.close()

        # Supprime le fichier si aucune puce forfait mobile
        if (written == 0):
            os.remove(csv_file)

