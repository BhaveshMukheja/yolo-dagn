import os
import shutil
import pandas as pd

# Update these paths
csv_main = "data/baselineModel/sample/sample.csv"          # CSV containing ObjID list
csv_lookup = "data/baselineModel/test/test.csv"      # CSV to search and copy rows from
image_root = r"D:\College\Research\\Astrophysics\ProjectTry\ModelMaking\\data\test"        # Root folder containing image subfolders
output_csv = "data/baselineModel/sample/merged.csv"
output_image_folder = "data/baselineModel/sample/selected_images/"

# Create output folder if it doesn't exist
os.makedirs(output_image_folder, exist_ok=True)

# -------------------------
# 1. Read CSV files
# -------------------------
df_main = pd.read_csv(csv_main)
df_lookup = pd.read_csv(csv_lookup)

# Ensure ObjID is string type
df_main['ObjID'] = df_main['ObjID'].astype(str).str.strip()
df_lookup['ObjID'] = df_lookup['ObjID'].astype(str).str.strip()

# -------------------------
# 2. Merge rows based on ObjID
# -------------------------
merged_df = df_main.merge(df_lookup, on="ObjID", how="left")

# Save merged CSV
merged_df.to_csv(output_csv, index=False)
print(f"Merged CSV saved: {output_csv}")

# -------------------------
# 3. Find and copy matching images
# -------------------------
obj_ids = set(df_main['ObjID'])

copied = 0

for root, dirs, files in os.walk(image_root):
    for file in files:
        name, ext = os.path.splitext(file)

        if name in obj_ids:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(output_image_folder, file)

            shutil.copy2(src_path, dst_path)
            copied += 1

print(f"Copied {copied} images to '{output_image_folder}'")