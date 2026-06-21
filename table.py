import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import math


branch_excel = "/Users/rachaelkim/BioM2Lab/Branch_label/metrics_measured_for_trimming_rachael.xlsx"
branches = pd.read_excel(branch_excel)

def prefix(csv_file):
    basename = csv_file.split('/')[-1]
    parts = basename.split('_')
    tree_num = parts[0][4:]
    side_code = parts[1]
    return f"T{tree_num}-{side_code}"


def append(csv_file, node_col="NODE_ID", dry_run=True, preview_rows=5):
    """
    Adds Branch ID to a single QSM node CSV based on a single branch Excel table.
    Automatically filters Excel for the correct tree based on CSV filename.

    csv_file: path to the QSM node CSV
    node_col: column in CSV that contains node numbers to match
    dry_run: if True, only prints preview; if False, updates CSV
    preview_rows: number of rows to show in preview
    """

    base_prefix = prefix(csv_file)

    tree_branches = branches[branches['Branch ID'].str.startswith(base_prefix, na=False)].copy()
    tree_branches['QSM_NODE'] = tree_branches['QSM_NODE'].astype(float)

    node_to_branch = tree_branches.drop_duplicates('QSM_NODE').set_index('QSM_NODE')['Branch ID'].to_dict()

    qsmnodes = pd.read_csv(csv_file)
    qsmnodes[node_col] = qsmnodes[node_col].astype(float)

    empty_mask = qsmnodes['Branch ID'].isna() | (qsmnodes['Branch ID'] == '')
    qsmnodes.loc[empty_mask, 'Branch ID'] = (
        qsmnodes.loc[empty_mask, node_col].map(node_to_branch).fillna('')
    )

    if dry_run:
        preview = qsmnodes[qsmnodes['Branch ID'] != '']
        print(f"\nPreview of {csv_file} (first {preview_rows} rows with Branch ID):")
        print(preview.head(preview_rows))
        print(f"Total rows with Branch ID: {len(preview)}")
    else:
        qsmnodes.to_csv(csv_file, index=False)
        print(f"Updated {csv_file} with Branch ID.")


def create_combined(output_file="/Users/rachaelkim/BioM2Lab/Branch_label/combined_node_branch.csv"):
    """
    Creates an empty combined CSV file with columns NODE_ID and Branch ID.
    Overwrites the file if it already exists.
    """
    df = pd.DataFrame(columns=["NODE_ID", "Branch ID"])
    df.to_csv(output_file, index=False)
    print(f"Created empty combined CSV at {output_file}")

def append2(branch_csv_file, combined_csv_file="/Users/rachaelkim/BioM2Lab/Branch_label/combined_node_branch.csv",
    node_col="NODE_ID", dry_run=True, preview_rows=10):
    """
    Appends rows with NODE_ID and Branch ID from a single branch CSV to the combined CSV.
    Only includes rows where Branch ID is not empty.

    branch_csv_file: path to the branch CSV with Branch ID appended
    combined_csv_file: path to the combined CSV file to append to
    dry_run: if True, only shows a preview without writing
    preview_rows: number of rows to show in preview
    """

    df_branch = pd.read_csv(branch_csv_file)
    df_branch = df_branch[df_branch['Branch ID'].notna() & (df_branch['Branch ID'] != '')]
    df_branch[node_col] = df_branch[node_col].astype(float).astype(int)
    df_branch = df_branch[[node_col, 'Branch ID']]

    if len(df_branch) == 0:
        print(f"No rows with Branch ID to add from {branch_csv_file}.")
        return

    df_combined = pd.read_csv(combined_csv_file)
    new_rows = df_branch.merge(df_combined, on=[node_col, 'Branch ID'], how='left', indicator=True)
    new_rows = new_rows[new_rows['_merge'] == 'left_only'].drop(columns=['_merge'])

    if len(new_rows) == 0:
        print(f"No new rows to add from {branch_csv_file}.")
        return

    if dry_run:
        print(f"\nPreview of rows to be added from {branch_csv_file} (first {preview_rows} rows):")
        print(new_rows.head(preview_rows))
        print(f"Total new rows to add: {len(new_rows)}")
    else:
        df_combined = pd.concat([df_combined, new_rows], ignore_index=True)
        df_combined.to_csv(combined_csv_file, index=False)
        print(f"Added {len(new_rows)} rows from {branch_csv_file} to {combined_csv_file}")


def append3(branch_csv_file, combined_csv_file="/Users/rachaelkim/BioM2Lab/Branch_label/combined_node_branch.csv",
    node_col="NODE_ID", dry_run=True, preview_rows=10):
    """
    Appends or updates rows with radius metrics:

        RADIUS_AREA_CM = sqrt(NODE_RADIUS_AREA / pi) * 100
        RADIUS_CIRC_CM = (NODE_RADIUS_CIRCUMFERENCE / (2*pi)) * 100

    NODE_RADIUS_AREA and NODE_RADIUS_CIRCUMFERENCE are in meters, so convert to cm.

    IF (NODE_ID, Branch ID) exists --> update radius values.
    If not --> append new row.
    """

    df_branch = pd.read_csv(branch_csv_file)

    df_branch = df_branch[df_branch["Branch ID"].notna() & (df_branch["Branch ID"] != "")]
    df_branch[node_col] = df_branch[node_col].astype(float).astype(int)

    if "NODE_RADIUS_AREA" in df_branch.columns:
        df_branch["RADIUS_AREA_CM"] = (
            np.sqrt(df_branch["NODE_RADIUS_AREA"] / np.pi) * 100
        )
    else:
        df_branch["RADIUS_AREA_CM"] = np.nan

    if "NODE_RADIUS_CIRCUMFERENCE" in df_branch.columns:
        df_branch["RADIUS_CIRC_CM"] = (
            (df_branch["NODE_RADIUS_CIRCUMFERENCE"] / (2 * np.pi)) * 100
        )
    else:
        df_branch["RADIUS_CIRC_CM"] = np.nan

    df_branch = df_branch[[node_col, "Branch ID", "RADIUS_AREA_CM", "RADIUS_CIRC_CM"]]

    try:
        df_combined = pd.read_csv(combined_csv_file)
    except FileNotFoundError:
        df_combined = pd.DataFrame(columns=[node_col, "Branch ID", "RADIUS_AREA_CM", "RADIUS_CIRC_CM"])

    for col in ["RADIUS_AREA_CM", "RADIUS_CIRC_CM"]:
        if col not in df_combined.columns:
            df_combined[col] = np.nan

    merged = df_branch.merge(
        df_combined[[node_col, "Branch ID"]],
        on=[node_col, "Branch ID"],
        how="left",
        indicator=True
    )

    to_add = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])
    to_update = merged[merged["_merge"] == "both"].drop(columns=["_merge"])

    if dry_run:
        print("\n=== ROWS TO ADD ===")
        print(to_add.head(preview_rows))
        print("Count:", len(to_add))

        print("\n=== ROWS TO UPDATE ===")
        print(to_update.head(preview_rows))
        print("Count:", len(to_update))
        return

    # Apply updates
    for _, row in to_update.iterrows():
        mask = (
            (df_combined[node_col] == row[node_col]) &
            (df_combined["Branch ID"] == row["Branch ID"])
        )
        df_combined.loc[mask, "RADIUS_AREA_CM"] = row["RADIUS_AREA_CM"]
        df_combined.loc[mask, "RADIUS_CIRC_CM"] = row["RADIUS_CIRC_CM"]

    df_combined = pd.concat([df_combined, to_add], ignore_index=True)

    df_combined.to_csv(combined_csv_file, index=False)

    print(f"Added {len(to_add)} rows and updated {len(to_update)} rows.")
    print(f"Saved to: {combined_csv_file}")


def append4(excel_file="/Users/rachaelkim/BioM2Lab/Branch_label/metrics_measured_for_trimming_rachael.xlsx",
    combined_csv_file="/Users/rachaelkim/BioM2Lab/Branch_label/combined_node_branch.csv",
    node_col="NODE_ID", dry_run=True, preview_rows=10):
    """
    Appends or updates rows with 'D1 (cm)' (diameter) converted to radius (cm):
        D1_radius = d1 (cm) / 2
    """
    df_excel = pd.read_excel(excel_file)
    df_excel = df_excel[df_excel["Branch ID"].notna() & (df_excel["Branch ID"] != "")]

    df_excel[node_col] = pd.to_numeric(df_excel['QSM_NODE'], errors='coerce')
    df_excel['D1 (cm)'] = pd.to_numeric(df_excel['D1 (cm)'], errors='coerce')

    df_excel['D1_radius'] = df_excel['D1 (cm)'] / 2

    df_excel = df_excel[[node_col, "Branch ID", "D1_radius"]].dropna(subset=[node_col])

    try:
        df_combined = pd.read_csv(combined_csv_file)
    except FileNotFoundError:
        df_combined = pd.DataFrame(columns=[node_col, "Branch ID", "D1_radius"])

    if "D1_radius" not in df_combined.columns:
        df_combined["D1_radius"] = pd.NA

    merged = df_excel.merge(
        df_combined[[node_col, "Branch ID"]],
        on=[node_col, "Branch ID"],
        how="left",
        indicator=True
    )

    to_add = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])
    to_update = merged[merged["_merge"] == "both"].drop(columns=["_merge"])

    if dry_run:
        print("\n=== ROWS TO ADD ===")
        print(to_add.head(preview_rows))
        print("Count:", len(to_add))

        print("\n=== ROWS TO UPDATE ===")
        print(to_update.head(preview_rows))
        print("Count:", len(to_update))
        return

    for _, row in to_update.iterrows():
        mask = (df_combined[node_col] == row[node_col]) & (df_combined["Branch ID"] == row["Branch ID"])
        df_combined.loc[mask, "D1_radius"] = row["D1_radius"]

    df_combined = pd.concat([df_combined, to_add], ignore_index=True)

    df_combined.to_csv(combined_csv_file, index=False)
    print(f"Added {len(to_add)} rows and updated {len(to_update)} rows.")
    print(f"Saved to: {combined_csv_file}")


def clean_combined_csv(combined_csv_file="/Users/rachaelkim/BioM2Lab/Branch_label/combined_node_branch.csv",
    dry_run=True, preview_rows=10):
    """
    Cleans the combined CSV by:
      1. Removing DIAM_AREA, DIAM_CIRC, and D1 columns (if they exist)
      2. Removing rows where BOTH RADIUS_AREA_CM and RADIUS_CIRC_CM are missing

    Parameters:
      combined_csv_file : path to the CSV
      dry_run : if True, shows preview but does NOT save
      preview_rows : number of preview rows to show
    """

    df = pd.read_csv(combined_csv_file)

    cols_to_drop = ["DIAM_AREA", "DIAM_CIRC", "D1"]
    existing = [c for c in cols_to_drop if c in df.columns]
    df_clean = df.drop(columns=existing)

    if "RADIUS_AREA_CM" not in df_clean.columns or "RADIUS_CIRC_CM" not in df_clean.columns:
        print("Missing radius columns. Cannot clean rows.")
        return

    mask_empty = df_clean["RADIUS_AREA_CM"].isna() & df_clean["RADIUS_CIRC_CM"].isna()
    num_to_remove = mask_empty.sum()

    print(f"Found {num_to_remove} rows with BOTH radius values missing.")

    if dry_run:
        print("\n=== Preview rows to be removed ===")
        print(df_clean[mask_empty].head(preview_rows))
        print("\n=== Columns after removal ===")
        print(df_clean.drop(df_clean[mask_empty].index).columns.tolist())
        return

    df_clean = df_clean[~mask_empty].reset_index(drop=True)
    df_clean.to_csv(combined_csv_file, index=False)

    print(f"Removed {num_to_remove} empty-radius rows.")
    print(f"Removed columns: {existing}")
    print(f"Saved cleaned CSV → {combined_csv_file}")


def append5(branch_csv_file, combined_csv_file="/Users/rachaelkim/BioM2Lab/Branch_label/combined_node_branch.csv",
    node_col="NODE_ID", dry_run=True, preview_rows=10):
    """
    Appends or updates rows with radius metrics in centimeters:
        RADIUS_AREA_CM = sqrt(NODE_RADIUS_AREA / pi) * 100
        RADIUS_CIRC_CM = NODE_RADIUS_CIRCUMFERENCE / (2 * pi) * 100

    If (NODE_ID, Branch ID) exists → update radius values.
    If not → append new row.
    """

    df_branch = pd.read_csv(branch_csv_file)

    df_branch = df_branch[df_branch["Branch ID"].notna() & (df_branch["Branch ID"] != "")]
    df_branch[node_col] = df_branch[node_col].astype(float).astype(int)

    df_branch["RADIUS_AREA_CM"] = (
        np.sqrt(df_branch["NODE_RADIUS_AREA"] / np.pi) * 100
        if "NODE_RADIUS_AREA" in df_branch.columns else np.nan
    )

    df_branch["RADIUS_CIRC_CM"] = (
        (df_branch["NODE_RADIUS_CIRCUMFERENCE"] / (2 * np.pi)) * 100
        if "NODE_RADIUS_CIRCUMFERENCE" in df_branch.columns else np.nan
    )

    df_branch = df_branch[[node_col, "Branch ID", "RADIUS_AREA_CM", "RADIUS_CIRC_CM"]]

    try:
        df_combined = pd.read_csv(combined_csv_file)
    except FileNotFoundError:
        df_combined = pd.DataFrame(columns=[node_col, "Branch ID", "RADIUS_AREA_CM", "RADIUS_CIRC_CM"])

    for col in ["RADIUS_AREA_CM", "RADIUS_CIRC_CM"]:
        if col not in df_combined.columns:
            df_combined[col] = np.nan

    merged = df_branch.merge(
        df_combined[[node_col, "Branch ID"]],
        on=[node_col, "Branch ID"],
        how="left",
        indicator=True
    )

    to_add = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])
    to_update = merged[merged["_merge"] == "both"].drop(columns=["_merge"])

    if dry_run:
        print("\n=== ROWS TO ADD ===")
        print(to_add.head(preview_rows))
        print("Count:", len(to_add))

        print("\n=== ROWS TO UPDATE ===")
        print(to_update.head(preview_rows))
        print("Count:", len(to_update))
        return

    for _, row in to_update.iterrows():
        mask = (
            (df_combined[node_col] == row[node_col]) &
            (df_combined["Branch ID"] == row["Branch ID"])
        )

        df_combined.loc[mask, "RADIUS_AREA_CM"] = row["RADIUS_AREA_CM"]
        df_combined.loc[mask, "RADIUS_CIRC_CM"] = row["RADIUS_CIRC_CM"]

    df_combined = pd.concat([df_combined, to_add], ignore_index=True)

    df_combined.to_csv(combined_csv_file, index=False)

    print(f"Added {len(to_add)} rows and updated {len(to_update)} rows.")
    print(f"Saved to: {combined_csv_file}")
