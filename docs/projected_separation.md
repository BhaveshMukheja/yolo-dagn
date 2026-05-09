# Projected Separation Estimation

After post-processing, projected angular and physical separations are computed for the final dual-nuclei detections.

The projected separation pipeline:

1. Reads YOLO OBB detections
2. Computes longest bounding-box edge lengths
3. Converts pixel separations to angular separations
4. Queries SDSS metadata
5. Converts angular separations to projected physical separations in kpc

---

## Script
[src/post-process/projected_separation.py](../src/post-process/projected_separation.py)


---

## Run Command

```bash id="j19x6k"
python src/post-process/projected_separation.py --config configs/post-process/projected_separation.yaml
```

---

## Example Configuration
[projected_separation.yaml](../configs/post-process/projected_separation.yaml)

---

## Methodology

### Longest Edge Estimation

For each OBB detection:

* YOLO normalized coordinates are converted into image-space coordinates
* polygon edge lengths are computed
* the maximum edge length is selected

This value is treated as the projected nuclei separation proxy.

---

### Pixel to Arcsecond Conversion

Angular separation is computed using:

```text id="2i5z2x"
dist_arcsec = pixel_distance × pixel_scale
```

where:

```text id="9v7b2n"
pixel_scale = 0.3 arcsec/pixel
```

---

### SDSS Metadata Retrieval

The script queries SDSS DR16 to retrieve:

* RA
* DEC
* spectroscopic redshift

using the object identifier (`ObjID`).

---

### Arcsecond to kpc Conversion

Physical projected separation is computed using:

* Flat ΛCDM cosmology
* angular diameter distance

via Astropy cosmology utilities.

---

## Output Catalog

Final catalog:

```text id="5zjlwm"
results/finalModel/projected_separations.csv
```

Contains:

| Column          | Description                          |
| --------------- | ------------------------------------ |
| ObjID           | SDSS object identifier               |
| RA              | Right ascension                      |
| DEC             | Declination                          |
| class           | YOLO class ID                        |
| Redshift        | Spectroscopic redshift               |
| longest_edge_px | Longest OBB edge length in pixels    |
| dist_arcsec     | Angular projected separation         |
| dist_kpc        | Physical projected separation in kpc |

---

## Notes

* Only `class 0` detections are processed during projected separation estimation.
* SDSS query retries and timeout handling are implemented for robustness.
* Intermediate catalogs are periodically saved during long runs.
* The final projected separation catalog is used for statistical analysis and visualization in the notebooks.
