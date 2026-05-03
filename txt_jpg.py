import os
import shutil

# مسیرات (update these)
source_folder = "data/finalModel/sample/selected_images"
jpg_folder = "jpg_files"
txt_folder = "txt_files"

# Create destination folders
os.makedirs(jpg_folder, exist_ok=True)
os.makedirs(txt_folder, exist_ok=True)

# Loop through files
for file in os.listdir(source_folder):
    src_path = os.path.join(source_folder, file)

    # Skip directories
    if not os.path.isfile(src_path):
        continue

    name, ext = os.path.splitext(file)

    ext = ext.lower()

    if ext == ".jpg":
        dst_path = os.path.join(jpg_folder, file)
        shutil.move(src_path, dst_path)

    elif ext == ".txt":
        dst_path = os.path.join(txt_folder, file)
        shutil.move(src_path, dst_path)

print("Done separating files!")