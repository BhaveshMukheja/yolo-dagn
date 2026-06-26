import pandas as pd
import numpy as np

# Input CSV file
input_file = "failed/projected_separations.csv"

# Output CSV file
output_file = "failed/projected_separations_s_kpc.csv"

# Read the CSV
df = pd.read_csv(input_file)

# Constant factor in the formula
factor = (np.pi * 1e3 * 3e5) / (180 * 3600 * 71)

# Calculate physical distance in kpc
df["delta_s_kpc"] = factor * df["dist_arcsec"] * df["Redshift"]

# Save to a new CSV
df.to_csv(output_file, index=False)

print(f"Done! Output saved to {output_file}")