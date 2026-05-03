import pandas as pd
import logging
from astroquery.sdss import SDSS
from astropy import coordinates as coords
import astropy.units as u

# -------------------------
# Setup logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("sdss_query.log"),
        logging.StreamHandler()
    ]
)

logging.info("Script started")

# ملفاتك (update paths)
input_csv = "data/finalModel/test.csv"
output_csv = "output_with_z.csv"

# -------------------------
# Load data
# -------------------------
logging.info("Loading CSV...")
df = pd.read_csv(input_csv)

df['RA'] = df['RA'].astype(float)
df['DEC'] = df['DEC'].astype(float)

logging.info(f"Loaded {len(df)} rows")

# -------------------------
# Query SDSS
# -------------------------
spec_ids = []

for i, row in df.iterrows():
    ra = row['RA']
    dec = row['DEC']

    logging.info(f"Processing index {i} | RA={ra}, DEC={dec}")

    try:
        pos = coords.SkyCoord(ra=ra*u.deg, dec=dec*u.deg)

        xid = SDSS.query_region(pos, radius=2*u.arcsec, spectro=True)

        if xid is not None and len(xid) > 0:
            spec_id = xid['z'][0]
            spec_ids.append(spec_id)
            logging.info(f"Match found: z={spec_id}")
        else:
            spec_ids.append(None)
            logging.warning("No match found")

    except Exception as e:
        logging.error(f"Error at index {i}: {e}")
        spec_ids.append(None)

# -------------------------
# Save results
# -------------------------
df['Redshift'] = spec_ids

logging.info("Saving output CSV...")
df.to_csv(output_csv, index=False)

logging.info(f"Finished. Output saved to {output_csv}")