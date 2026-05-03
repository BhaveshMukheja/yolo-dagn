import pandas as pd

# ملفاتك (update path)
input_csv = "data/finalModel/sample/sample.csv"
output_csv = "output_with_labels.csv"

# Load data
df = pd.read_csv(input_csv)
df["RA"] = df["RA"].astype(float)
df["DEC"] = df["DEC"].astype(float)
# Define mapping
class_map = {
    0: "Dual Nuclei",
    1: "Galaxy nucleus + star",
    2: "Nucleus + unidentified",
    3: "Single nucleus"
}

col = "Class (From SDSS)"

# -------------------------
# 1. Frequency count (numeric)
# -------------------------
print("\nFrequency (numeric):")
print(df[col].value_counts().sort_index())

# -------------------------
# 2. Replace with labels
# -------------------------
df[col] = df[col].map(class_map)

# -------------------------
# 3. Frequency count (text)
# -------------------------
print("\nFrequency (labels):")
print(df[col].value_counts())

# -------------------------
# 4. Save CSV
# -------------------------
df.to_csv(output_csv, index=False)

print(f"\nSaved updated CSV to: {output_csv}")