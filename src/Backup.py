"""
Script Name: Copy Files Utility
Description: A utility script to copy files from a source directory to a destination directory.
Usage: python Backup.py -s <source_directory> -d <destination_directory> [-w] [-m] [-r]

Arguments:
  -s <source_directory>     : Specify the source directory for copying files.
  -d <destination_directory>: Specify the destination directory for copied files.
  -r                        : Rename all copied files as (1, 2, 3 ... n)
  -w                        : Activate WhatsApp end notification mode.
  -m                        : Activate mail end notification mode.

Example Usages:
  python Backup.py -s /path/to/source -d /path/to/destination -m
  python Backup.py -s source_folder -d destination_folder -w -r

Notes:
  - The '-s' and '-d' flags are mandatory.
"""
import pywhatkit
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


def notify_was():

    phone_number = "+34XXXXXXXXX"
    pywhatkit.sendwhatmsg_instantly(
        phone_number, "Back up finalizado", tab_close=True, close_time=0)


def notify_mail():
    print("notify_mail not implemented")


def count_files_to_copy(path):
    file_list = []
    for (current_dir, directories, files) in os.walk(path):
        file_list.extend(files)
    return len(file_list)


def copy_files(source, destination, rename):
    if rename:
        file_counter = load_counter()
    total_files = count_files_to_copy(source)
    copied_files = 0
    print("TotalFiles: ", total_files)
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
            shutil.copy2(source_path, destination_path)
            if rename:
                save_counter(file_counter)

        copied_files += len(files)
        print("Saved: ", round(copied_files/total_files*100, 2),
              "%", "=> ", copied_files, "/", total_files, "\n")


if __name__ == "__main__":
    was = "-w" in sys.argv
    mail = "-m" in sys.argv
    rename = "-r" in sys.argv

    if "-s" in sys.argv and "-d" in sys.argv:
        source_directory = sys.argv[sys.argv.index("-s") + 1]
        destination_directory = sys.argv[sys.argv.index("-d") + 1]
    else:

        source_directory = input("Source directory: ")
        destination_directory = input("Destination directory: ") or source_directory+"Copy"

    counter_location = destination_directory+"/counter.txt"
    copy_files(source_directory, destination_directory, rename)

    if mail:
        notify_mail()
    if was:
        notify_was()
