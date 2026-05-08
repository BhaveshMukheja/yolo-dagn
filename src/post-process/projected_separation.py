import argparse
import csv
import logging
import math
import os
import time
from glob import glob

import requests
import yaml

from astropy import units as u
from astropy.cosmology import FlatLambdaCDM

# ============================================================
# ARGPARSE
# ============================================================

parser = argparse.ArgumentParser(
    description="Generate projected separation catalog "
                "from YOLO OBB predictions."
)

parser.add_argument(
    "--config",
    type=str,
    required=True,
    help="Path to YAML config file"
)

args = parser.parse_args()

# ============================================================
# LOAD CONFIG
# ============================================================

with open(args.config, "r") as f:
    CONFIG = yaml.safe_load(f)

# ============================================================
# CONFIG VARIABLES
# ============================================================

LABELS_DIR = CONFIG["labels_dir"]

OUTPUT_CSV = CONFIG["output_csv"]

IMAGE_SIZE = CONFIG["image_size"]

PIXEL_SCALE = CONFIG["pixel_scale_arcsec"]

TARGET_CLASS = CONFIG["target_class"]

SAVE_EVERY = CONFIG["save_every"]

LOG_LEVEL = CONFIG["log_level"]

SDSS_URL = CONFIG["sdss"]["sql_url"]

REQUEST_TIMEOUT = CONFIG["sdss"]["timeout"]

MAX_RETRIES = CONFIG["sdss"]["max_retries"]

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============================================================
# COSMOLOGY
# ============================================================

COSMOLOGY = FlatLambdaCDM(
    H0=CONFIG["cosmology"]["H0"],
    Om0=CONFIG["cosmology"]["Om0"]
)

# ============================================================
# REQUEST SESSION
# ============================================================

session = requests.Session()

# ============================================================
# SDSS QUERY
# ============================================================

def get_sdss_metadata(objid):

    query = (
        "SELECT TOP 1 "
        "p.objID, "
        "p.ra, "
        "p.dec, "
        "s.z "
        "FROM PhotoObj AS p "
        "JOIN SpecObj AS s "
        "ON p.objID = s.bestObjID "
        f"WHERE p.objID = {objid}"
    )

    # Remove accidental whitespace/newlines
    query = " ".join(query.split())

    params = {
        "cmd": query,
        "format": "json"
    }

    for attempt in range(MAX_RETRIES):

        try:

            response = session.get(
                SDSS_URL,
                params=params,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            data = response.json()

            if not data:
                return None

            rows = data[0].get("Rows", [])

            if len(rows) == 0:
                return None

            row = rows[0]

            return (
                float(row["ra"]),
                float(row["dec"]),
                float(row["z"])
            )

        except Exception as e:

            logging.warning(
                f"[{objid}] "
                f"Retry {attempt+1}/{MAX_RETRIES} "
                f"failed: {e}"
            )

            time.sleep(1)

    logging.error(
        f"[{objid}] SDSS query failed."
    )

    return None

# ============================================================
# OBB GEOMETRY
# ============================================================

def calculate_longest_edge(coords):
    """
    Compute longest edge from YOLO OBB coordinates.

    coords:
        [x1 y1 x2 y2 x3 y3 x4 y4]
        normalized between 0 and 1
    """

    pixels = [

        (
            coords[i] * IMAGE_SIZE,
            coords[i + 1] * IMAGE_SIZE
        )

        for i in range(0, 8, 2)
    ]

    edges = [

        math.dist(
            pixels[i],
            pixels[(i + 1) % 4]
        )

        for i in range(4)
    ]

    return max(edges)

# ============================================================
# ARCSEC -> KPC
# ============================================================

def angular_to_kpc(arcsec, redshift):
    """
    Convert angular separation to projected
    physical separation in kpc.
    """

    theta = arcsec * u.arcsec

    angular_distance = (
        COSMOLOGY.angular_diameter_distance(
            redshift
        )
    )

    physical_size = (
        theta * angular_distance
    ).to(
        u.kpc,
        u.dimensionless_angles()
    )

    return physical_size.value

# ============================================================
# SAVE CSV
# ============================================================

def save_catalog(rows):

    os.makedirs(
        os.path.dirname(OUTPUT_CSV),
        exist_ok=True
    )

    with open(
        OUTPUT_CSV,
        "w",
        newline=""
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "ObjID",
            "RA",
            "DEC",
            "class",
            "Redshift",
            "longest_edge_px",
            "dist_arcsec",
            "dist_kpc"
        ])

        writer.writerows(rows)

# ============================================================
# MAIN PIPELINE
# ============================================================

def process_labels():

    label_files = glob(
        os.path.join(
            LABELS_DIR,
            "*.txt"
        )
    )

    total_files = len(label_files)

    logging.info(
        f"Found {total_files} label files."
    )

    if total_files == 0:

        logging.error(
            "No label files found."
        )

        return

    rows = []

    processed = 0
    failed = 0

    for idx, label_file in enumerate(label_files):

        objid = os.path.splitext(
            os.path.basename(label_file)
        )[0]

        try:

            with open(label_file, "r") as f:

                lines = f.readlines()

            if len(lines) == 0:
                continue

            for line in lines:

                parts = line.strip().split()

                # Need:
                # class + 8 coordinates
                if len(parts) < 9:

                    logging.warning(
                        f"[{objid}] "
                        f"Malformed label."
                    )

                    continue

                try:

                    class_id = int(parts[0])

                except Exception:

                    logging.warning(
                        f"[{objid}] "
                        f"Invalid class id."
                    )

                    continue

                # Only target class
                if class_id != TARGET_CLASS:
                    continue

                try:

                    coords = list(
                        map(float, parts[1:9])
                    )

                except Exception:

                    logging.warning(
                        f"[{objid}] "
                        f"Invalid coordinates."
                    )

                    continue

                # ====================================================
                # LONGEST EDGE
                # ====================================================

                longest_edge_px = (
                    calculate_longest_edge(
                        coords
                    )
                )

                # ====================================================
                # PIXEL -> ARCSEC
                # ====================================================

                dist_arcsec = (
                    longest_edge_px
                    * PIXEL_SCALE
                )

                # ====================================================
                # SDSS METADATA
                # ====================================================

                metadata = get_sdss_metadata(objid)

                if metadata is None:

                    failed += 1

                    continue

                ra, dec, z = metadata

                # Skip invalid redshift
                if z <= 0:

                    failed += 1

                    continue

                # ====================================================
                # ARCSEC -> KPC
                # ====================================================

                dist_kpc = angular_to_kpc(
                    dist_arcsec,
                    z
                )

                # ====================================================
                # SAVE ROW
                # ====================================================

                rows.append([

                    str(objid),

                    round(ra, 6),

                    round(dec, 6),

                    class_id,

                    round(z, 6),

                    round(longest_edge_px, 4),

                    round(dist_arcsec, 4),

                    round(dist_kpc, 4)
                ])

            processed += 1

            # ========================================================
            # PERIODIC SAVE
            # ========================================================

            if processed % SAVE_EVERY == 0:

                logging.info(
                    f"Processed "
                    f"{processed}/{total_files}"
                )

                save_catalog(rows)

        except Exception as e:

            failed += 1

            logging.error(
                f"[{objid}] "
                f"Failed processing: {e}"
            )

    # ============================================================
    # FINAL SAVE
    # ============================================================

    save_catalog(rows)

    logging.info("================================")
    logging.info("PROCESS COMPLETE")
    logging.info("================================")

    logging.info(
        f"Successfully processed: {processed}"
    )

    logging.info(
        f"Failed: {failed}"
    )

    logging.info(
        f"Final catalog saved to:\n"
        f"{OUTPUT_CSV}"
    )

# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":

    process_labels()