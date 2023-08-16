import os
import hashlib
import sys


def find_duplicates_by_name(directory, verbose, of):
    seen_files = {}

    for root, _, files in os.walk(directory):
        for file in files:

            full_path = os.path.join(root, file)

            if not file in seen_files.keys():
                seen_files[file] = []
            seen_files[file].append(
                os.path.relpath(full_path, directory))

    #Show verbose
    if verbose and not of:
        for key in seen_files.keys():
            if len(seen_files[key]) > 1:
                print("Key:", key, "; Count:", len(seen_files[key]), ";")
                for path in seen_files[key]:
                    print(path)
        print("\n\n")

    #Write output on file (Shows verbose avoiding loop twice)
    if of:
        with open(of, "w", encoding='utf-8') as f:
            for key in seen_files.keys():
                if len(seen_files[key]) > 1:
                    print("Key:", key, "; Count:", len(seen_files[key]),";", file=f)
                    if verbose:
                        print("Key:", key, "; Count:",
                              len(seen_files[key]), ";")
                    for path in seen_files[key]:
                        if verbose:
                            print(path)
                        print(path, file=f)
    return seen_files


def calculate_sha256(file_path, block_size=65536):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            sha256_hash.update(block)

    return sha256_hash.hexdigest()


def find_duplicates_by_hash(directory, verbose):
    hash_map = {}
    duplicate_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            
            full_path = os.path.join(root, file)
            file_hash = calculate_sha256(full_path)

            if file_hash in hash_map:
                duplicate_files.append((os.path.relpath(
                    full_path, directory), os.path.relpath(hash_map[file_hash], directory)))
            else:
                hash_map[file_hash] = full_path
    if verbose:
        for a, b in duplicate_files:
            print("Hash Repetido: ", a, "===", b)
    return duplicate_files


if __name__ == "__main__":

    #Checks directory by arg
    if "-d" in sys.argv:
        search_directory = sys.argv[sys.argv.index("-d") + 1]
    else:
        #Ask for directory if -d was not used
        search_directory = input("Destination directory: ")
        if not os.path.isabs(search_directory):
            raise Exception("Path not abs")
        
    #Checks verbose option
    if "-v" in sys.argv:
        verbose = True
    else:
        verbose = False

    #Checks OutputFile Option
    if "-of" in sys.argv:
        of = sys.argv[sys.argv.index("-of") + 1]
    else:
        of = False

    find_duplicates_by_name(search_directory, verbose, of)

    # find_duplicates_by_hash(search_directory, verbose, of)
