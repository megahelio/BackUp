"""
Script Name: Copy Files Utility
Description: A utility script to copy files.
Usage: python Backup.py -s <source_directory> -d <destination_directory> [-r] [-w] [-m] [-nd] [-dd]

Arguments:
  -s <source_directory>         : Specify the source directory for copying files.
  -d <destination_directory>    : Specify the destination directory for copied files.
  -r                            : Rename all copied files as (1, 2, 3 ... n)
  -w                            : Activate WhatsApp end notification mode.
  -m                            : Activate mail end notification mode.
  -nd                           : Prevent copying duplicate files.
  -dd                           : Delete duplicated files from the destination directory.

Example Usages:
  python Backup.py -s /path/to/source -d /path/to/destination -m
  python Backup.py -s source_folder -d destination_folder -w -r -nd -dd

Notes:
  - The '-s' and '-d' flags are mandatory.
"""
import pywhatkit
import os
import sys
import shutil
import json
import hashlib
from tqdm import tqdm


def get_counter(file_location):
    try:
        with open(file_location, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 1


def get_sha256_dict_destination(file_location, destination_path):
    try:
        with open(file_location, 'r') as file:
            sha256_dict_destination = json.load(file)
            return sha256_dict_destination
    except FileNotFoundError:
        sha256_dict_destination = {}

        print(count_files(destination_path),
              " != ", len(sha256_dict_destination))
        if os.path.exists(destination_path) and os.path.isdir(destination_path):
            if count_files(destination_path) != len(sha256_dict_destination):
                sha256_dict_destination = {}
                total_files = count_files(destination_path)
                with tqdm(total=total_files, desc="Searching Hashes", unit="file") as pbar:
                    for root, _, files in os.walk(destination_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            file_hash = calculate_sha256(full_path)

                            if not file_hash in sha256_dict_destination:
                                sha256_dict_destination[file_hash] = []
                            sha256_dict_destination[file_hash].append(
                                os.path.relpath(full_path, destination_path))

                            pbar.update(1)
                    save_sha256_dict(file_location=sha256_location,
                                     sha256_dict=sha256_dict_destination)
        return sha256_dict_destination


def save_sha256_dict(file_location, sha256_dict):
    with open(file_location, 'w') as file:
        json.dump(sha256_dict, file)


def save_counter(data, file_output):
    with open(file_output, "w") as f:
        f.write(str(data))


def notify_was():

    phone_number = "+34XXXXXXXXX"
    pywhatkit.sendwhatmsg_instantly(
        phone_number, "Back up finalizado", tab_close=True, close_time=0)


def notify_mail():
    print("notify_mail not implemented")


def count_files(path):
    file_list = []
    for (current_dir, directories, files) in os.walk(path):
        file_list.extend(files)
    return len(file_list)


def calculate_sha256(file_path, block_size=65536):
    """
    Calculate the SHA-256 hash of a file.

    :param file_path: Path to the file.
    :param block_size: Block size for reading the file.
    :return: SHA-256 hash of the file.
    """
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            sha256_hash.update(block)
    return sha256_hash.hexdigest()


def update_sha256_json(file_location, destination_path):

    sha256_dict_destination = {}
    total_files = count_files(destination_path)
    with tqdm(total=total_files, desc="Updating Hashes", unit="file") as pbar:
        for root, _, files in os.walk(destination_path):
            for file in files:
                full_path = os.path.join(root, file)
                file_hash = calculate_sha256(full_path)

                if not file_hash in sha256_dict_destination:
                    sha256_dict_destination[file_hash] = []
                sha256_dict_destination[file_hash].append(
                    os.path.relpath(full_path, destination_path))

                pbar.update(1)
        save_sha256_dict(file_location=file_location,
                         sha256_dict=sha256_dict_destination)
    return sha256_dict_destination


def delete_duplicated(path, sha256dict):
    print(sha256dict)
    for key in tqdm(sha256dict.keys(), desc="Searching and removing duplicated files:", unit="hash", total=len(sha256dict.keys())):
        if len(sha256dict[key]) > 1:

            for file in sha256dict[key][1:]:
                print("Deleting:", os.path.join(path, file))
                try:
                    os.remove(os.path.join(path, file))
                except:
                    print("Unable to delete", os.path.join(path, file))
            unique_path = sha256dict[key][0]
            sha256dict[key].clear()
            sha256dict[key] = [unique_path]

    print(sha256dict)
    eliminar_carpetas_vacias(path)


def eliminar_carpetas_vacias(ruta_directorio):
    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_directorio, topdown=False):
        for subcarpeta in subcarpetas:
            ruta_completa = os.path.join(carpeta_actual, subcarpeta)
            if not os.listdir(ruta_completa):  # Verificar si la carpeta está vacía
                try:
                    os.rmdir(ruta_completa)  # Eliminar la carpeta vacía
                    print(f"Se ha eliminado la carpeta vacía: {ruta_completa}")
                except OSError as e:
                    print(f"No se pudo eliminar la carpeta {ruta_completa}:")


def copy_files(source, destination, rename, no_duplicate, delete_duplicade):
    if rename:
        file_counter = get_counter(counter_location)
    if no_duplicate:
        sha256_dict_destination = get_sha256_dict_destination(
            file_location=sha256_location, destination_path=destination)

    print(sha256_dict_destination)
    total_files_to_copy = count_files(source)
    copied_files = 0
    files_skipped_counter = 0
    print("TotalFiles: ", total_files_to_copy)
    for root, directories, files in os.walk(source):

        for file in tqdm(files, desc="Coping: "+os.path.relpath(root, source), unit="file", total=len(files)):
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source)
            dir_name = os.path.dirname(relative_path)
            # Generate a new name for the file using an incrementing counter
            if rename:
                file_extension = os.path.splitext(file)[1]
                destination_filename = f"{file_counter}{file_extension}"
                file_counter += 1
            else:
                destination_filename = f"{file}"
            destination_path = os.path.join(
                destination, dir_name, destination_filename)
            # Create destination folder if it doesn't exist
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            hash_file_to_copy = calculate_sha256(os.path.join(root, file))

            # Si el fichero no existe se copia
            if no_duplicate and not hash_file_to_copy in sha256_dict_destination:
                # Primero se copia porque es la operación que lleva más tiempo y es crítica (no quiero tener hashes/contadores de ficheros que se interrumpio su copia)
                shutil.copy2(source_path, destination_path)
                copied_files += 1
                # Agregar "sha256_fichero_copiado" : "ruta_donde_se_copia" al diccionario (previene arrastrar duplicados de la carpeta de origen)
                sha256_dict_destination[hash_file_to_copy] = destination_path
                if rename:
                    save_counter(file_counter, counter_location)
            # Si el fichero está duplicado
            else:
                if rename:
                    file_counter -= 1
                files_skipped_counter += 1
                print(os.path.join(root, file), "already exists on",
                      sha256_dict_destination[calculate_sha256(os.path.join(root, file))])

        # Calcular porcentaje
        try:
            percent = round(copied_files/(total_files_to_copy -
                                          files_skipped_counter)*100, 2)
        except ZeroDivisionError:
            percent = 100
        print("Saved: ", percent, "%", "=> ", copied_files, "/", total_files_to_copy -
              files_skipped_counter)
        print("Skipped:", files_skipped_counter, "files")

        if delete_duplicade or no_duplicate:
            sha256_dict_destination = update_sha256_json(sha256_location, destination)
        if delete_duplicade:
            delete_duplicated(path=destination, sha256dict=sha256_dict_destination)


if __name__ == "__main__":
    was = "-w" in sys.argv
    mail = "-m" in sys.argv
    rename = "-r" in sys.argv
    no_duplicate = "-nd" in sys.argv
    delete_duplicade = "-dd" in sys.argv

    if "-s" in sys.argv and "-d" in sys.argv:
        source_directory = sys.argv[sys.argv.index("-s") + 1]
        destination_directory = sys.argv[sys.argv.index("-d") + 1]
    else:

        source_directory = input("Source directory: ")
        destination_directory = input(
            "Destination directory: ") or source_directory+"Copy"

    sha256_location = destination_directory+"/sha256.json"
    counter_location = destination_directory+"/counter.txt"
    copy_files(source_directory, destination_directory, rename, no_duplicate,delete_duplicade)

    if mail:
        notify_mail()
    if was:
        notify_was()
