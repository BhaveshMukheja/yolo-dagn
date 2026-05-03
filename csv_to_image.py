import os
import shutil
import pandas as pd

# -------------------------
# Config
# -------------------------
input_csv = "input.csv"
image_root = "images/"              # folder containing images (may have subfolders)
output_folder = "selected_images/"
objid_column = "ObjID"

# Create output folder
os.makedirs(output_folder, exist_ok=True)

# -------------------------
# Load CSV (keep as string!)
# -------------------------
df = pd.read_csv(input_csv, dtype=str)

# Clean ObjID values
obj_ids = set(df[objid_column].str.strip())

print(f"Loaded {len(obj_ids)} unique ObjIDs")

# -------------------------
# Build image lookup map
# -------------------------
image_map = {}

for root, dirs, files in os.walk(image_root):
    for file in files:
        name, ext = os.path.splitext(file)
        image_map[name.strip()] = os.path.join(root, file)

print(f"Indexed {len(image_map)} images")

# -------------------------
# Copy matching images
# -------------------------
copied = 0
missing = 0

for obj_id in obj_ids:
    if obj_id in image_map:
        src = image_map[obj_id]
        dst = os.path.join(output_folder, os.path.basename(src))

        shutil.copy2(src, dst)
        copied += 1
    else:
        missing += 1

print("\nDone!")
print(f"Copied: {copied}")
print(f"Missing: {missing}")