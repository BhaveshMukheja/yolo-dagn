import pandas as pd

# Load CSVs
god = pd.read_csv("updated_star.csv")
ref = pd.read_csv("results/finalModel/post-filter/pure_dual_nuclei.csv")  # the one containing matching ObjIDs

# Ensure ObjID is same type in both
god["ObjID"] = god["ObjID"].astype(str)
ref["ObjID"] = ref["ObjID"].astype(str)

# Find matching ObjIDs
matching_ids = set(ref["ObjID"])

# Fill the column where ObjID matches
god.loc[god["ObjID"].isin(matching_ids), "Class (From YOLO Model)"] = "Dual Nuclei"

# Save result
god.to_csv("detections_with_boob.csv", index=False)

print("Done! Updated file saved as updated_god.csv")