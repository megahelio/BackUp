import os
import hashlib
import sys
from tqdm import tqdm

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


def find_duplicates_by_hash(directory, verbose, of):
    """
    Find and display or save duplicate files by their SHA-256 hash in the given directory.

    :param directory: The directory to search for duplicate files.
    :param verbose: A boolean indicating whether to display detailed output.
    :param of: An optional output file name where results will be saved.
    :return: A list of duplicate files found.
    """
    hash_map = {}
    duplicate_files = []

    # Calculate the total number of files to show the global loading bar
    total_files = sum(len(files) for _, _, files in os.walk(directory))

    with tqdm(total=total_files, desc="Searching Hashes", unit="file") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:

                full_path = os.path.join(root, file)
                file_hash = calculate_sha256(full_path)

                if not file_hash in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(
                    os.path.relpath(full_path, directory))

                pbar.update(1)

    if verbose:
        print("Sha256\tFiles")
        for key in hash_map.keys():
            print(key, end="\t")
            for file in hash_map[key]:
                print(file, end="\t")
            print()
    if of:
        with open(of, "a", encoding='utf-8') as f:
            print("Sha256\tFiles", file=f)
            for key in hash_map.keys():
                print(key, file=f, end="\t")
                for file in hash_map[key]:
                    print(file, file=f, end="\t")
                print(file=f)

    return duplicate_files


if __name__ == "__main__":

    # Checks directory by arg
    if "-d" in sys.argv:
        search_directory = sys.argv[sys.argv.index("-d") + 1]
    else:
        # Ask for directory if -d was not used
        search_directory = input("Destination directory: ")
        if not os.path.isabs(search_directory):
            raise Exception("Path not abs")

    # Checks verbose option
    if "-v" in sys.argv:
        verbose = True
    else:
        verbose = False

    # Checks OutputFile Option
    if "-of" in sys.argv:
        of = sys.argv[sys.argv.index("-of") + 1]
        with open(of, "w", encoding='utf-8') as f:
            print(file=f, end="")
    else:
        of = False

    find_duplicates_by_hash(search_directory, verbose, of)
