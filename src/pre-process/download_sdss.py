import os
import time
import yaml
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm


FAILED_LOG = "failed_downloads.txt"


# ---------------------------
# Config Loader
# ---------------------------
def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


# ---------------------------
# Fetch Image with Retry
# ---------------------------
def fetch_image(base_url, ra, dec, cfg):
    url = (
        f"{base_url}?ra={ra}&dec={dec}"
        f"&scale={cfg['scale']}"
        f"&width={cfg['width']}"
        f"&height={cfg['height']}"
    )

    for attempt in range(cfg["max_retries"]):
        try:
            response = requests.get(url, timeout=cfg["timeout"])

            if response.status_code == 200:
                return Image.open(BytesIO(response.content))

            else:
                print(f"[WARN] HTTP {response.status_code}")

        except requests.exceptions.RequestException:
            print("[WARN] Connection error")

        # exponential backoff
        sleep_time = cfg["backoff_factor"] ** attempt
        time.sleep(sleep_time)

    return None


# ---------------------------
# Failure Logger
# ---------------------------
def save_failure(obj_id, ra, dec):
    with open(FAILED_LOG, "a") as f:
        f.write(f"{obj_id},{ra},{dec}\n")


# ---------------------------
# Validate Columns
# ---------------------------
def validate_columns(df, col_map):
    required = ["obj_id", "ra", "dec"]

    for key in required:
        if key not in col_map:
            raise ValueError(f"Missing column mapping: {key}")

        if col_map[key] not in df.columns:
            raise ValueError(f"Column '{col_map[key]}' not found in CSV")


# ---------------------------
# Process DataFrame
# ---------------------------
def process_dataframe(df, save_dir, sdss_cfg, col_map):
    os.makedirs(save_dir, exist_ok=True)

    for _, row in tqdm(df.iterrows(), total=len(df)):
        obj_id = str(row[col_map["obj_id"]])
        ra = row[col_map["ra"]]
        dec = row[col_map["dec"]]

        save_path = os.path.join(save_dir, f"{obj_id}.jpg")

        # ✅ Resume support
        if os.path.exists(save_path):
            continue

        img = fetch_image(
            sdss_cfg["base_url"],
            ra,
            dec,
            {
                **sdss_cfg["image"],
                **sdss_cfg["request"],
            },
        )

        if img:
            img.save(save_path)
        else:
            save_failure(obj_id, ra, dec)

        # ✅ Rate limiting
        time.sleep(sdss_cfg["request"]["delay_between_requests"])


# ---------------------------
# Main Download Logic
# ---------------------------
def download_dataset(name, config):
    dataset = config["datasets"][name]
    sdss_cfg = config["sdss"]

    # ✅ Column mapping (dataset override OR global fallback)
    col_map = dataset.get("columns", config["columns"])

    df = pd.read_csv(dataset["csv_path"], dtype={col_map["obj_id"]: str})

    # ✅ Clean column names (important!)
    df.columns = df.columns.str.strip()

    # ✅ Validate required columns
    validate_columns(df, col_map)

    # ✅ Limit rows if specified
    if dataset.get("limit"):
        df = df.iloc[: dataset["limit"]]

    batch_size = dataset.get("batch_size")

    if batch_size:
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i : i + batch_size]
            print(f"\n[INFO] Processing batch {i} → {i + len(batch)}")

            process_dataframe(batch, dataset["save_dir"], sdss_cfg, col_map)
    else:
        process_dataframe(df, dataset["save_dir"], sdss_cfg, col_map)


# ---------------------------
# Retry Failed Downloads
# ---------------------------
def retry_failed(config):
    if not os.path.exists(FAILED_LOG):
        print("No failed downloads found.")
        return

    print("[INFO] Retrying failed downloads...")

    col_map = config["columns"]

    df = pd.read_csv(
        FAILED_LOG,
        names=[
            col_map["obj_id"],
            col_map["ra"],
            col_map["dec"],
        ],
    )

    process_dataframe(df, "data/raw/retries", config["sdss"], col_map)


# ---------------------------
# CLI Entry Point
# ---------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--retry_failed", action="store_true")

    args = parser.parse_args()

    config = load_config(args.config)

    if args.retry_failed:
        retry_failed(config)
    else:
        if not args.dataset:
            raise ValueError("Please provide --dataset name")

        download_dataset(args.dataset, config)