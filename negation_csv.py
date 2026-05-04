import pandas as pd

# Load files
god = pd.read_csv("detections_with_boob.csv")
subset = pd.read_csv("data/finalModel/bootstrapped_data.csv")

# Ensure same column order (important!)
subset = subset[god.columns]

# Remove duplicates just in case
god = god.drop_duplicates()
subset = subset.drop_duplicates()

# Find rows in god that are NOT in subset
merged = god.merge(subset, how='left', indicator=True)

output = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

# Save result
output.to_csv("raw_detections.csv", index=False)

print("Done! Saved rows not in subset to output.csv")