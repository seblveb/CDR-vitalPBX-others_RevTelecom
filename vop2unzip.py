
# native
import zipfile

# Unzips file and returns the directory, named after the zip file itself
def unzip_file(path: str) -> str :
    with zipfile.ZipFile(path, 'r') as zip_ref:
        directory = path.removesuffix(".zip")
        zip_ref.extractall(directory)
    return directory
