# Python utilities

---

## Duplicate File Finder by Hash (Duplicated_Hash)

This Python script is designed to identify and manage duplicate files within a specified directory based on their SHA-256 hash values. It can display the duplicate files' information on the console or save the results to an output file.

### Prerequisites

- Python 3.x installed on your system.
- Required Python packages: `os`, `hashlib`, `sys`, and `tqdm`. You can install these packages using pip: `pip install tqdm`.

### Usage

To use this script, follow the steps below:

1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the script with the following command:

   ```
   python Duplicated_Hash.py -d directory_path [-v] [-of output_file]
   ```

   Replace `directory_path` with the absolute path of the directory you want to search for duplicate files.

   Optional arguments:

   - `-v`: Display detailed information about duplicate files on the console.
   - `-of output_file`: Save the results to the specified output file.
4. If you do not provide the `-v` argument, the script will automatically search for duplicate files by their SHA-256 hash values and display progress using a loading bar.
5. After completion, the script will provide a summary of duplicate files found, listing their SHA-256 hash values and corresponding file paths.

### Examples

#### Example 1: Displaying Duplicate Files on Console

Command:

```bash
python duplicate_finder_by_hash.py -d /path/to/directory -v
```

Output:

```
Searching Hashes: 100%|█████████████████████████████████████| 8/8 [00:00<00:00, 208.35file/s]
Sha256          Files
d1a7f60...       file1.txt    file2.txt
f0b43d9...       file3.txt    subdir/file3.txt
```

#### Example 2: Saving Duplicate File Information to an Output File

Command:

```bash
python duplicate_finder_by_hash.py -d /path/to/directory -of duplicates.txt
```

Content of `duplicates.txt`:

```
Sha256          Files
d1a7f60...       file1.txt    file2.txt
f0b43d9...       file3.txt    subdir/file3.txt
```
- Note: The actual SHA-256 hash values and filenames in the examples will differ based on the files in your specified directory. These examples demonstrate the format of the output and the information provided by each script.


### Notes


- The script recursively searches for files in the specified directory and its subdirectories.
- The SHA-256 hash is used to compare files, ensuring accurate identification of duplicates.
- If using the `-of` option, the script will append results to the output file if it already exists.
- Be cautious when deleting files based on the provided information. Always verify the results before taking any action.

For further assistance, please refer to the script's source code or contact the developer.

---

## Duplicate File Finder by Name

This Python script is designed to search and manage duplicate files within a specified directory based on their filenames. It can display the duplicate files' information on the console or save the results to an output file.

### Prerequisites

- Python 3.x installed on your system.
- Required Python packages: `os`, `sys`, and `tqdm`. You can install the `tqdm` package using pip: `pip install tqdm`.

### Usage

To use this script, follow the steps below:

1. Open a terminal or command prompt.

2. Navigate to the directory where the script is located.

3. Run the script with the following command:

    ```
    python Duplicated_Name.py -d directory_path [-v] [-of output_file]
    ```

    Replace `Duplicated_Name.py` with the actual name of the script file.

    Replace `directory_path` with the absolute path of the directory you want to search for duplicate files.

    Optional arguments:
    
    - `-v`: Display detailed information about duplicate files on the console.
    - `-of output_file`: Save the results to the specified output file.

4. If you do not provide the `-v` argument, the script will automatically search for duplicate files by their filenames and display progress using a loading bar.

5. After completion, the script will provide a summary of duplicate files found, listing their filenames and corresponding file paths.

### Examples

#### Example 1: Displaying Duplicate Files on Console

Command:

```bash
python duplicate_finder_by_name.py -d /path/to/directory -v
```

Output:

```
Searching Names: 100%|██████████████████████████████████| 6/6 [00:00<00:00, 6002.34file/s]
Key: file1.txt    Count: 2    file1.txt    subdir1/file1.txt
```

#### Example 2: Saving Duplicate File Information to an Output File

Command:

```bash
python duplicate_finder_by_name.py -d /path/to/directory -of duplicates.txt
```

Content of `duplicates.txt`:

```
Key: file1.txt    Count: 2    file1.txt    subdir1/file1.txt
```

### Notes

- The script recursively searches for files in the specified directory and its subdirectories.
- Be cautious when deleting files based on the provided information. Always verify the results before taking any action.

For further assistance, please refer to the script's source code or contact the developer.

---

## BackUp

Simple back up Python Script

The resulting script copies the contents of the "source" path (files and directories) maintaining the folder structure and renaming the files incrementally. Finally it saves in "./counter.txt" the last value o the incremental from where it will be counted. At the end of the copy, if you have it configured, a WhatssApp message will be sent.

I had a lot of images and videos with names generated incretingly by the camera and I wanted to create a copy without the problem of two files having the same name.

![Ejemplo Salida](https://github.com/megahelio/BackUp/assets/47276914/57edf460-1197-4849-a6d7-d525ff2979be)

---
