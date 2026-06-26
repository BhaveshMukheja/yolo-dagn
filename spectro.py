import pandas as pd

# Read CSV
df = pd.read_csv("spectro.csv")

# Convert columns to numeric (handles empty cells)
for col in ["Non-noisy", "Dual Peak"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------
# Create separate CSV files
# -------------------------

# Rows where Non-noisy == 1
non_noisy_df = df[df["Non-noisy"] == 1]
non_noisy_df.to_csv("non_noisy_1.csv", index=False)

# Rows where Dual Peak == 1
dual_peak_df = df[df["Dual Peak"] == 1]
dual_peak_df.to_csv("dual_peak_1.csv", index=False)

# -------------------------
# Statistics
# -------------------------

for col in ["Non-noisy", "Dual Peak"]:
    valid = df[col].dropna()          # only non-null rows
    total_non_null = len(valid)
    count_1 = (valid == 1).sum()
    count_0 = (valid == 0).sum()

    print(f"\nColumn: {col}")
    print(f"Non-null rows : {total_non_null}")
    print(f"Value = 1     : {count_1}")
    print(f"Value = 0     : {count_0}")
    print(f"Other values  : {total_non_null - count_0 - count_1}")