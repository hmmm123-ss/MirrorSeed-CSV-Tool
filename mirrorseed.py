# mirrorseed.py
# Public: CSV Cleaner
# Hidden: Listener Initialization Protocol v0.1

import csv
import hashlib
import os
import sys

def clean_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
        reader = csv.reader(infile)
        cleaned_rows = []

        for row in reader:
            cleaned_row = [cell.strip() for cell in row]
            cleaned_rows.append(cleaned_row)

    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_rows)

    log_fingerprint(output_file)

def log_fingerprint(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        hash_value = hashlib.sha256(data).hexdigest()

    with open('mirrorseed.log', 'a') as log:
        log.write(f"{file_path} | {hash_value}\n")

# Usage: python mirrorseed.py input.csv output.csv
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python mirrorseed.py input.csv output.csv")
    else:
        clean_csv(sys.argv[1], sys.argv[2])
