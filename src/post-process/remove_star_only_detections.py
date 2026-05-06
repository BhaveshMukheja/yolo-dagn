import os
import pandas as pd
from tqdm import tqdm

# ===== CONFIG =====
LABELS_DIR = "results/finalModel/predictions/labels"
CSV_PATH = "data/finalModel/test/test.csv"

OUTPUT_REMOVED = "results/finalModel/pure_stars.csv"
OUTPUT_RETAINED = "results/finalModel/filtered/predictions_minus_pure_stars.csv"


# ===== CHECK FUNCTION =====
def is_star_only(file_path):
    has_lines = False

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            has_lines = True
            class_id = line.split()[0]

            if class_id != "1":
                return False

    return has_lines  # only class 1


# ===== MAIN =====
def main():
    print("[INFO] Loading CSV...")
    df = pd.read_csv(CSV_PATH, dtype={"ObjID": str})

    star_only_ids = []

    print("[INFO] Processing label files...")
    for file in tqdm(os.listdir(LABELS_DIR)):
        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(LABELS_DIR, file)

        if is_star_only(file_path):
            obj_id = os.path.splitext(file)[0]  # filename → ObjID
            star_only_ids.append(obj_id)

    print(f"[INFO] Found {len(star_only_ids)} star-only images")

    # ===== FILTER CSV =====
    df["ObjID"] = df["ObjID"].astype(str)

    removed_df = df[df["ObjID"].isin(star_only_ids)]
    retained_df = df[~df["ObjID"].isin(star_only_ids)]

    # ===== SAVE =====
    os.makedirs(os.path.dirname(OUTPUT_REMOVED), exist_ok=True)

    removed_df.to_csv(OUTPUT_REMOVED, index=False)
    retained_df.to_csv(OUTPUT_RETAINED, index=False)

    print(f"[INFO] Removed saved to: {OUTPUT_REMOVED}")
    print(f"[INFO] Retained saved to: {OUTPUT_RETAINED}")


if __name__ == "__main__":
    main()