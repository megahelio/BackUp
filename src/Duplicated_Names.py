import os
import sys
from tqdm import tqdm


def find_duplicates_by_name(directory, verbose, of):
    """
     Search and display or save to file duplicate files by name in the given directory.

     :param directory: The directory in which to search for duplicates.
     :param verbose: Boolean indicating whether to display verbose output to the console.
     :param of: Optional filename where the results will be saved.
     :return: A dictionary containing the duplicate files by name found.
     """
    seen_files = {}

    # Calculate the total number of files to show the global loading bar
    total_files = sum(len(files) for _, _, files in os.walk(directory))

    with tqdm(total=total_files, desc="Searching Names", unit="file") as pbar:
        for root, dirnames, files in os.walk(directory):
            for file in files:

                full_path = os.path.join(root, file)

                if not file in seen_files.keys():
                    seen_files[file] = []
                seen_files[file].append(
                    os.path.relpath(full_path, directory))
                pbar.update(1)

    # Show verbose
    if verbose and not of:
        for key in seen_files.keys():
            if len(seen_files[key]) > 1:
                print("Key:", key, "Count:",
                      len(seen_files[key]), end="\t")
                for path in seen_files[key]:
                    print(path, end="\t")
        print("\n\n")

    # Write output on file (Shows verbose avoiding loop twice)
    if of:
        with open(of, "a", encoding='utf-8') as f:
            for key in tqdm(seen_files.keys(), desc="Writing Output", unit="file", total=len(seen_files.keys())):
                if len(seen_files[key]) > 1:
                    print("Key:", key, "Count:",
                          len(seen_files[key]), end="\t", file=f)
                    if verbose:
                        print("Key:", key, "Count:",
                              len(seen_files[key]), end="\t")
                    for path in seen_files[key]:
                        if verbose:
                            print(path, end="\t")
                        print(path, file=f, end="\t")
                    print("\n", file=f)
    return seen_files


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

    find_duplicates_by_name(search_directory, verbose, of)
