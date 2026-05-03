import os
import pandas as pd

# Paths
input_csv = r"D:\College\Research\\Astrophysics\ProjectTry\ModelMaking\\47k_ObjID__RA_DEC.csv"
image_folder = r"D:\College\Research\\Astrophysics\ProjectTry\ModelMaking\yolo_Model_2\\data\test"
output_csv = "data/finalModel/test.csv"

# Read CSV (keep as string to avoid scientific notation issues)
df = pd.read_csv(input_csv, dtype=str)

# -------------------------
# Get ALL image filenames recursively
# -------------------------
valid_ids = set()

for root, dirs, files in os.walk(image_folder):
    for file in files:
        name, ext = os.path.splitext(file)
        valid_ids.add(name)

print(f"Found {len(valid_ids)} image IDs")

# -------------------------
# Filter CSV
# -------------------------
filtered_df = df[df['ObjID'].str.strip().isin(valid_ids)]

# Save
filtered_df.to_csv(output_csv, index=False)

print(f"Saved {len(filtered_df)} rows to {output_csv}")