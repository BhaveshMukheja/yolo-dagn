# Dataset Preparation

The repository uses SDSS imaging data stored as CSV catalogs. Images are downloaded using object identifiers (`ObjID`) along with their corresponding celestial coordinates (`RA`, `DEC`) and organized into YOLO-compatible directory structures.

The same download pipeline is used for both the baseline and final models through the shared download script:

```bash
python src/pre-process/download_sdss.py
```

---

# Expected Dataset Structure

```text
data/
├── baselineModel/
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   ├── val/
│   │   ├── images/
│   │   └── labels/
│   └── test/
│       └── images/
│
└── finalModel/
    ├── train/
    │   ├── images/
    │   └── labels/
    ├── val/
    │   ├── images/
    │   └── labels/
    └── test/
        └── images/
```

---

# Configuration Files

Dataset definitions and download parameters are configured through YAML configuration files:

- Baseline model configuration: [`baselineModel.yaml`](../configs/data/baselineModel.yaml)
- Final model configuration: [`finalModel.yaml`](../configs/data/finalModel.yaml)

These configuration files define:
- CSV catalog locations
- image output directories
- SDSS download parameters
- batching limits
- coordinate column mappings

---

# Running the Download Script

Example:

```bash
python src/pre-process/download_sdss.py --config configs/data/finalModel.yaml --dataset train
```

---

# Script Arguments

| Argument | Description |
|---|---|
| `--config` | Path to the dataset configuration YAML file |
| `--dataset` | Dataset split or catalog to download |

---

# SDSS Download Configuration

The downloader retrieves SDSS DR16 image cutouts using the SDSS SkyServer API.

Example configuration:

```yaml
sdss:
  base_url: "http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg"

  image:
    width: 120
    height: 120
    scale: 0.3

  request:
    timeout: 10
    max_retries: 5
    backoff_factor: 2
    delay_between_requests: 0.2
```

---

# CSV Column Mapping

The downloader supports configurable CSV column mappings:

```yaml
columns:
  obj_id: "ObjID"
  ra: "RA"
  dec: "DEC"
```

This allows the pipeline to adapt to catalogs with different column naming conventions.

---

# Dataset Definitions

Each dataset split or catalog is defined independently within the configuration file.

Example:

```yaml
datasets:
  train:
    csv_path: "data/finalModel/train/train.csv"
    save_dir: "data/finalModel/train/images"
    limit: null

  val:
    csv_path: "data/finalModel/val/val.csv"
    save_dir: "data/finalModel/val/images"
    limit: null

  test:
    csv_path: "data/finalModel/test/test.csv"
    save_dir: "data/finalModel/test/images"
    limit: null
    batch_size: 5000
```

---

# Notes

- Download destinations can be modified directly from the YAML configuration files.
- Large datasets may optionally be downloaded in batches.
- The repository only provides CSV catalogs and annotations. SDSS image cutouts must be downloaded separately using the provided scripts.
- Label files should remain aligned with the corresponding image directories for YOLO training compatibility.