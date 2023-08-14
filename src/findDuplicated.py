import os
import hashlib
import sys


def find_duplicates_by_name(directory):
    seen_names = set()
    duplicate_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            # print(root, file)
            full_path = os.path.join(root, file)
            if file in seen_names:
                duplicate_files.append(os.path.relpath(full_path, directory))
            else:
                seen_names.add(file)

    return duplicate_files


def calculate_file_hash(file_path, block_size=65536):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            sha256_hash.update(block)

    return sha256_hash.hexdigest()


def find_duplicates_by_hash(directory):
    hash_map = {}
    duplicate_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            # print(root, file)
            full_path = os.path.join(root, file)
            file_hash = calculate_file_hash(full_path)

            if file_hash in hash_map:
                duplicate_files.append((os.path.relpath(
                    full_path, directory), os.path.relpath(hash_map[file_hash], directory)))
            else:
                hash_map[file_hash] = full_path

    return duplicate_files


if __name__ == "__main__":

    if "-d" in sys.argv:
        search_directory = sys.argv[sys.argv.index("-d") + 1]
    else:
        search_directory = input("Destination directory: ")
        if not os.path.isabs(search_directory):
            raise Exception("Path not abs")

    print("Finding duplicates by name:")
    name_duplicates = find_duplicates_by_name(search_directory)
    for duplicate in name_duplicates:
        print(duplicate)

    print("\nFinding duplicates by hash:")
    hash_duplicates = find_duplicates_by_hash(search_directory)
    for file1, file2 in hash_duplicates:
        print(file1, file2)
