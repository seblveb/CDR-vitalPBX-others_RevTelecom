#!/usr/bin/python3

#own
from vop2pdf_parse import parse_arguments
from vop2pdf_make_graph import make_graph
from vop2pdf_make_csv import make_csv
from vop2unzip import unzip_file

#native
from datetime import timezone, datetime as dt
from collections import defaultdict
from pathlib import Path
from csv import reader
import locale
import os


def print_debug(string:str = ""):
    if (args.debug == True):
        print("DBG:{}".format(string))


def create_outputs(infos: list, conso: dict, total: dict, horodate: dict):

    # Converts strftime calls to french
    locale.setlocale(locale.LC_ALL, "fr_FR")

    # Converts values to lists
    data_d = list(conso.values())
    data_t = list(total.values())
    date = list(horodate.values())

    full_date = [dt.fromtimestamp(x * 21600, tz=timezone.utc).replace(tzinfo=None)  for x in horodate.keys()]

    # Defines date markers to base the graph title on
    month_year = full_date[0].strftime("%B %Y").capitalize()

    out = "{}/{}/{}".format(args.output_dir, infos[1], month_year, infos[2], infos[0], infos[3])
    # Creates output directory
    Path(out).mkdir(parents=True, exist_ok=True)

    # Creates the graph title
    title = ("{} - Consommation de 4G en Mo - {}\n".format(infos[2], month_year))

    print_debug("Making '{}'".format(title[:-1]))
    make_graph(title, date, data_d, data_t, out)
    make_csv(title, full_date, data_d, data_t, out)


def structure_data(file_path: str, conso: dict, source_file):

    first = list(conso)[0]
    last = list(conso)[-1]
    total = defaultdict(float)
    horodate = defaultdict(str)

    # Gets client infos from source file
    try :
        infos = [x for x in source_file if get_phone(file_path) in x][0]
    except :
        print("file {} has no attributed client".format(file_path))
        return

    # fills missing days if there are any
    for delta in range(first, last):
        if delta not in conso:
            conso[delta] = 0

    # sorts dictionnary to display it correctly
    consort = dict(sorted(conso.items()))

    # fills total with data equivalent and date depending on delta
    for i in range(first, last + 1):
        total[i] = round(consort[i] + (total[i - 1] if len(total) > 0 else 0), 2)
        date = dt.fromtimestamp(i * 21600, tz=timezone.utc)
        horodate[i] = "{:02d}/{:02d} | {:02d}H-{:02d}H".format(date.day, date.month, date.hour, date.hour + 6)

    print_debug("range data conso {}, total {}".format(len(conso), len(total))) # => DEBUG

    create_outputs(infos, consort, total, horodate)


def input_formatting(file_path: str, source_file, client_name: str=None) :

    print_debug("looking at {} :".format(file_path.split('/')[-1])) # => DEBUG

    with open(file_path) as csvfile :

        # Lis le header et skip les en-têtes
        csvreader = reader(csvfile)
        next(csvreader)

        # Initialise le dictionnaire avec des valeurs flottantes par défaut
        dict_conso = defaultdict(float)

        for row in csvreader :
            # Récupère la date en format datetime
            dt_obj = dt.strptime(row[2], '%Y-%m-%d %H:%M:%S')

            # Crée un delta arrondi en tranches de 6H en temps epoch                ? Ajouter flag pour tranche de temps de 24h ?
            delta = int(dt_obj.replace(tzinfo=timezone.utc).timestamp() / (6 * 3600))

            # Ajoute la consommation au delta actuel
            dict_conso[delta] = round(dict_conso[delta] + float(row[3]), 2)

    structure_data(file_path, dict_conso, source_file)


def subfinder(mylist, pattern):
    return list(filter(lambda x: x in pattern, mylist))

# Isole le numéro du téléphone du nom de fichier
get_phone = lambda x : x.split('-')[-1][:-4]

# Récupère une list de toutes les infos d'une colonne de double liste
get_listlist_row = lambda lst, i: list(list(zip(*lst))[i])

if __name__ == "__main__" :
    args = parse_arguments()

    # Récupère les numéros du fichier source
    with open(args.source_file) as source_file :
        source_reader = reader(source_file)
        next(source_reader)
        source = [row for row in source_reader]
        source_phone = [row[0] for row in source]

    # Créer le dossier d'output - À définir
    if not args.output_dir:
        args.output_dir = "out"

    dir = unzip_file(args.zip_file)

    files = [dir + "/" + f for f in os.listdir(dir)
            if "DATA" in f and get_phone(f) in source_phone]

    print_debug("\nDBG:".join(files))
    for f in files :
        input_formatting(f, source)

    nextcloud_path = "/var/www/html/nextcloud/occ"

    # ADAPTER SI BESOIN
    if (args.nextcloud_user):
        command = "sudo -u www-data php7.4 {} files:scan {}".format(nextcloud_path, args.nextcloud_user)
        print_debug("Command would be : {}".format(command))
        # os.execve(command)
    #if user:
        # sudo -u www-data php7.4 /var/www/html/nextcloud/occ files:scan CDR
