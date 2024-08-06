
# native
from argparse import ArgumentParser as argp
from os.path import isdir, isfile

# Vérifie que l'input est un chemin
def dir_path(string):
    if isdir(string):
        return string
    else:
        raise argp.error()

def file_path(string):
    if isfile(string):
        return string
    else:
        raise argp.error()

# Récupère les arguments de dossier et le booléen de debug
def parse_arguments():
    parser = argp()
    parser.add_argument("source_file", help="File with input clients", type=file_path)
    parser.add_argument("zip_file", help="Zip of RevTelecom data files to convert", type=file_path)
    parser.add_argument("-m", "--margin", help="Percentage of margin", type=int)
    parser.add_argument("-d", "--debug", help="Enables debug prints", action="store_true")
    parser.add_argument("-o", "--output_dir",help="Output directory, defaults to 'zip file name'_out")
    args = parser.parse_args()
    return args
