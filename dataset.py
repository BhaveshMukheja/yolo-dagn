import pandas as pd

# =========================
# CONFIG
# =========================
SOURCE_CSV = r"results\finalModel\total_without_duplicates.csv"   # CSV containing ObjID, RA, DEC
TARGET_CSV = r"results/finalModel/dual_nuclei.csv"   # CSV where you want to add/update RA, DEC
OUTPUT_CSV = r"results/finalModel/separations.csv"

# =========================
# LOAD FILES
# =========================
source_df = pd.read_csv(SOURCE_CSV)
target_df = pd.read_csv(TARGET_CSV)

# Normalize column names (optional but useful)
source_df.columns = source_df.columns.str.strip()
target_df.columns = target_df.columns.str.strip()

# Ensure required columns exist
required_source = {"ObjID", "Redshift", "dist_arcsec", "dist_kpc"}
required_target = {"ObjID"}

missing_source = required_source - set(source_df.columns)
missing_target = required_target - set(target_df.columns)

if missing_source:
    raise ValueError(f"Missing columns in source CSV: {missing_source}")

if missing_target:
    raise ValueError(f"Missing columns in target CSV: {missing_target}")

# =========================
# MERGE RA and DEC
# =========================
# Keep only needed columns from source
# ObjID,RA,DEC,Redshift,dist_arcsec,dist_kpc
source_subset = source_df[["ObjID", "Redshift", "dist_arcsec", "dist_kpc"]]

# Merge into target
merged_df = target_df.merge(source_subset, on="ObjID", how="left")

# =========================
# SAVE OUTPUT
# =========================
merged_df.to_csv(OUTPUT_CSV, index=False)

print(f"Saved merged CSV to: {OUTPUT_CSV}")