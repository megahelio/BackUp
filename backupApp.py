import os
import sys
import shutil
from tqdm import tqdm


def save_counter(counter):
    with open(counter_location, "w") as f:
        f.write(str(counter))


def load_counter():
    try:
        with open(counter_location, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 1


def count_files_to_copy(path):
    file_list = []
    for (current_dir, directories, files) in os.walk(path):
        file_list.extend(files)
    return len(file_list)


def copy_files(source, destination):
    file_counter = load_counter()
    total_files = count_files_to_copy(source)
    print("TotalFiles: ", total_files)

    for root, directories, files in tqdm(os.walk(source), unit="file", total=total_files):
        for file in tqdm(files, desc="Coping: "+os.path.relpath(root, source), unit="file", total=len(files)):
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source)
            dir_name = os.path.dirname(relative_path)
            file_extension = os.path.splitext(file)[1]
            # Generar un nuevo nombre para el archivo usando un contador incremental
            destination_filename = f"{file_counter}{file_extension}"
            file_counter += 1
            destination_path = os.path.join(
                destination, dir_name, destination_filename)
            # Crear la carpeta de destino si no existe
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.copy2(source_path, destination_path)
            save_counter(file_counter)

    


if __name__ == "__main__":

    if len(sys.argv) == 3:
        source_directory = sys.argv[1]
        destination_directory = sys.argv[2]
    else:
        default_source_directory = "C:/Users/Oscar/Desktop/test"
        default_destination_directory = default_source_directory+"Copy"
        source_directory = input(
            f"Source directory [{default_source_directory}]: ") or default_source_directory
        destination_directory = input(
            f"Destination directory [{default_destination_directory}]: ") or default_destination_directory

        # source_directory = default_source_directory
        # destination_directory = default_destination_directory
    counter_location = destination_directory+"/counter.txt"
    copy_files(source_directory, destination_directory)
