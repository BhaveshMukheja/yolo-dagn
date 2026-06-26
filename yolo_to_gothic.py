import pandas as pd
import numpy as np

# ------------------------------------------------------------------
# Input/output files
# ------------------------------------------------------------------
INPUT_CSV = "failed/projected_separations_s_kpc.csv"
OUTPUT_CSV = "gothic_catalog_failed.csv"

# ------------------------------------------------------------------
# Read catalog
# ------------------------------------------------------------------
df = pd.read_csv(INPUT_CSV)

# ------------------------------------------------------------------
# Convert YOLO -> GOTHIC separations
#
# Angular:
# theta_GOTHIC = 1.1698 * theta_YOLO - 4.8283
#
# Physical:
# s_GOTHIC = 0.66 * s_YOLO
# ------------------------------------------------------------------

df["gothic_dist_arcsec"] = (
    1.1698 * df["dist_arcsec"] - 4.8283
)

df["gothic_delta_s_kpc"] = (
    0.66 * df["delta_s_kpc"]
)

# Optional: prevent unphysical negative angular separations
df["gothic_dist_arcsec"] = np.clip(
    df["gothic_dist_arcsec"],
    a_min=0.0,
    a_max=None
)

# ------------------------------------------------------------------
# Save
# ------------------------------------------------------------------
df.to_csv(OUTPUT_CSV, index=False)

print(f"Saved: {OUTPUT_CSV}")
print(f"Objects processed: {len(df)}")