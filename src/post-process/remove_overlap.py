import os
import pandas as pd
from shapely.geometry import Polygon
from tqdm import tqdm


# =========================
# CONFIG
# =========================
LABELS_DIR = "GOTHIC/predictions/labels"

INPUT_CSV = "GOTHIC/filtered/predictions_minus_pure_stars.csv"

OUTPUT_OVERLAP = "GOTHIC/galaxy_star_intesections.csv"
OUTPUT_FINAL = "GOTHIC/dual_nuclei.csv"


# =========================
# Parse OBB line safely
# =========================
def parse_obb_line(line):
    parts = line.strip().split()

    if len(parts) < 9:
        return None

    try:
        cls = int(float(parts[0]))
        coords = list(map(float, parts[1:9]))

        points = [(coords[i], coords[i + 1]) for i in range(0, 8, 2)]

        poly = Polygon(points)

        # Fix invalid polygons
        if not poly.is_valid:
            poly = poly.buffer(0)

        return cls, poly

    except Exception:
        return None


# =========================
# Check overlap (optimized)
# =========================
def has_class_overlap(file_path):
    class0 = []
    class1 = []

    with open(file_path, "r") as f:
        for line in f:
            parsed = parse_obb_line(line)
            if not parsed:
                continue

            cls, poly = parsed

            if cls == 0:
                class0.append(poly)
            elif cls == 1:
                class1.append(poly)

    if not class0 or not class1:
        return False

    # Check intersections
    for p0 in class0:
        for p1 in class1:
            if p0.intersects(p1):
                if p0.intersection(p1).area > 0:
                    return True

    return False


# =========================
# MAIN
# =========================
def main():
    print("[INFO] Loading CSV...")
    df = pd.read_csv(INPUT_CSV, dtype={"ObjID": str})

    overlap_ids = []

    print("[INFO] Checking overlaps...")
    label_files = [f for f in os.listdir(LABELS_DIR) if f.endswith(".txt")]

    for file in tqdm(label_files):
        file_path = os.path.join(LABELS_DIR, file)

        if has_class_overlap(file_path):
            obj_id = os.path.splitext(file)[0]
            overlap_ids.append(obj_id)

    print(f"[INFO] Found {len(overlap_ids)} overlapping images")

    # =========================
    # FILTER CSV
    # =========================
    df["ObjID"] = df["ObjID"].astype(str)

    overlap_df = df[df["ObjID"].isin(overlap_ids)]
    final_df = df[~df["ObjID"].isin(overlap_ids)]

    # =========================
    # SAVE
    # =========================
    os.makedirs(os.path.dirname(OUTPUT_OVERLAP), exist_ok=True)

    overlap_df.to_csv(OUTPUT_OVERLAP, index=False)
    final_df.to_csv(OUTPUT_FINAL, index=False)

    print(f"[INFO] Overlap removed saved to: {OUTPUT_OVERLAP}")
    print(f"[INFO] Final dataset saved to: {OUTPUT_FINAL}")


if __name__ == "__main__":
    main()