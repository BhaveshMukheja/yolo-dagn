import os
import csv

INPUT_FILE = "only_class_1_files.txt"   # your txt file
OUTPUT_FILE = "filenames.csv"

filenames = []

with open(INPUT_FILE, "r") as f:
    for line in f:
        path = line.strip()
        if not path:
            continue

        # Extract filename without extension
        name = os.path.splitext(os.path.basename(path))[0]
        filenames.append([name])  # as row

# Write to CSV
with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["filename"])  # header
    writer.writerows(filenames)

print(f"Saved {len(filenames)} filenames to {OUTPUT_FILE}")