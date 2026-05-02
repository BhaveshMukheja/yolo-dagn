import os
import pandas as pd

# Paths (update these)
input_csv = r"data/baselineModel/681_from_GOTHIC.csv"
image_folder = r"D:\College\Research\\Astrophysics\ProjectTry\ModelMaking\\data\val\images"   # folder containing your images
output_csv = "data/baselineModel/val/val.csv"

# Read CSV
df = pd.read_csv(input_csv)

# Get list of image filenames (without extension)
image_files = os.listdir(image_folder)

# Create a set of valid ObjIDs (strip extensions)
valid_ids = set(os.path.splitext(img)[0] for img in image_files)

# Filter rows where ObjID exists in image folder
filtered_df = df[df['ObjID'].astype(str).isin(valid_ids)]

# Save to new CSV
filtered_df.to_csv(output_csv, index=False)

print(f"Saved {len(filtered_df)} rows to {output_csv}")