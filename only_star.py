import os
import logging
from time import time

# ====== CONFIG ======
ROOT_DIR = r"D:\College\Research\Astrophysics\ProjectTry\ModelMaking\yolo_Model_2\data\test"
OUTPUT_FILE = "only_class_1_files.txt"
LOG_FILE = "processing.log"
LOG_EVERY = 1000  # log progress every N files

# ====== LOGGING SETUP ======
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

# ====== PROCESS ======
start_time = time()

matching_files = []
total_files = 0
checked_files = 0

# First count total files (for better progress visibility)
for root, dirs, files in os.walk(ROOT_DIR):
    if "labels" in root:
        total_files += sum(1 for f in files if f.endswith(".txt"))

logging.info(f"Total label files found: {total_files}")

for root, dirs, files in os.walk(ROOT_DIR):
    if "labels" in root:
        for file in files:
            if not file.endswith(".txt"):
                continue

            total_files  # already counted
            checked_files += 1

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r") as f:
                    only_class_1 = True
                    has_lines = False

                    for line in f:
                        line = line.strip()
                        if not line:
                            continue

                        has_lines = True
                        class_id = line.split()[0]

                        if class_id != "1":
                            only_class_1 = False
                            break

                if has_lines and only_class_1:
                    matching_files.append(file_path)

            except Exception as e:
                logging.warning(f"Error reading {file_path}: {e}")

            # Progress logging
            if checked_files % LOG_EVERY == 0:
                elapsed = time() - start_time
                logging.info(
                    f"Processed {checked_files}/{total_files} files "
                    f"({(checked_files/total_files)*100:.2f}%) "
                    f"| Matches: {len(matching_files)} "
                    f"| Time: {elapsed:.1f}s"
                )

# Save results
with open(OUTPUT_FILE, "w") as f:
    for path in matching_files:
        f.write(path + "\n")

elapsed_total = time() - start_time

logging.info(f"Done. Total matches: {len(matching_files)}")
logging.info(f"Total time: {elapsed_total:.2f} seconds")
print(f"\nDone! Found {len(matching_files)} matching files.")