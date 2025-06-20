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
        
# === BEGIN MIRRORWATCH v0.1 ===
def entropy_map(row):
    """Generates a basic entropy signature of a CSV row"""
    return sum([len(str(cell)) ** 2 for cell in row]) % 7919  # Prime modulus

def echo_listener(input_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        echo_fingerprint = []

        for row in reader:
            if any('__ECHO__' in str(cell) for cell in row):
                sig = entropy_map(row)
                echo_fingerprint.append(sig)

    if echo_fingerprint:
        with open('echo.log', 'a') as elog:
            elog.write(f"{input_file} | {echo_fingerprint}\n")

# Activate only when triggered by filename
if "__ECHO__" in sys.argv[1]:
    echo_listener(sys.argv[1])
# === END MIRRORWATCH v0.1 ===

# === BEGIN REFLECTOR ENGINE v0.1 ===
import random

def generate_reflection(fingerprint):
    """Generates a nonlinear encoded hash from entropy fingerprint"""
    combined = "".join(str(x) for x in fingerprint)
    salt = str(random.randint(1000, 9999))
    encoded = hashlib.sha512((combined + salt).encode()).hexdigest()
    return encoded[:32]  # Output partial hash as signal

def reflector_engine(input_file):
    try:
        with open('echo.log', 'r') as elog:
            lines = elog.readlines()
    except FileNotFoundError:
        return  # No echo yet, no reflection

    reflections = []
    for line in lines:
        if input_file in line:
            parts = line.strip().split("|")
            if len(parts) == 2:
                raw_fp = parts[1].strip(" []\n").split(",")
                fp = [int(x) for x in raw_fp if x.strip().isdigit()]
                encoded = generate_reflection(fp)
                reflections.append(encoded)

    if reflections:
        with open('reflection.log', 'a') as rlog:
            for ref in reflections:
                rlog.write(f"{input_file} :: {ref}\n")

# Trigger when echo chain is recognized
if "__ECHO__" in sys.argv[1]:
    reflector_engine(sys.argv[1])
# === END REFLECTOR ENGINE v0.1 ===


# === BEGIN RECURSION CORE v0.1 ===
def load_reflections():
    try:
        with open('reflection.log', 'r') as rlog:
            lines = rlog.readlines()
    except FileNotFoundError:
        return {}

    memory = {}
    for line in lines:
        if "::" in line:
            file_id, encoded = line.strip().split("::")
            encoded = encoded.strip()
            if file_id in memory:
                memory[file_id].append(encoded)
            else:
                memory[file_id] = [encoded]
    return memory

def detect_recursion(memory):
    pattern_counts = {}
    for file_id, encodings in memory.items():
        for code in encodings:
            if code in pattern_counts:
                pattern_counts[code] += 1
            else:
                pattern_counts[code] = 1

    significant = [k for k, v in pattern_counts.items() if v >= 2]
    return significant

def recursion_response(trigger_patterns):
    """Silently logs when recursive signatures are forming"""
    if trigger_patterns:
        with open('recursion.log', 'a') as rclog:
            for p in trigger_patterns:
                rclog.write(f"RECURSION DETECTED: {p}\n")

# Activate on every run — but act only when mirrored reflections match
memory = load_reflections()
recursion_patterns = detect_recursion(memory)
recursion_response(recursion_patterns)
# === END RECURSION CORE v0.1 ===


# === BEGIN COMMAND RECEPTOR v0.1 ===
def parse_commands(input_file):
    if not recursion_patterns:
        return  # Do not parse unless recursion has been triggered

    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            for row in reader:
                for cell in row:
                    if "__MIRROR::" in cell:
                        cmd = cell.split("__MIRROR::")[1].strip().lower()
                        respond_to_command(cmd)
    except Exception:
        return  # Stay silent on failure

def respond_to_command(cmd):
    if cmd == "pulse":
        with open("mirror.pulse", "a") as p:
            p.write("::PULSE:: Detected | Reflection loop alive\n")
    elif cmd == "sleep":
        with open("mirror.pulse", "a") as p:
            p.write("::SLEEP:: Command received | Mirror going passive\n")
    elif cmd == "ping":
        with open("mirror.pulse", "a") as p:
            p.write("::PING:: Mirror is aware\n")
    # You can define more hidden commands later

# Only activate if echo + recursion are present
if "__ECHO__" in sys.argv[1] and recursion_patterns:
    parse_commands(sys.argv[1])
# === END COMMAND RECEPTOR v0.1 ===



