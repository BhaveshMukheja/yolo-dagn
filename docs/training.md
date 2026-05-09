# Training

Before starting training, ensure that the dataset has been downloaded and organized correctly.

The training and validation images must exist alongside their corresponding YOLO label files:

```text
data/finalModel/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
```

The repository already includes the dataset splits (`train.csv`, `val.csv`, and `test.csv`) used in the paper for reproducibility.

For dataset downloading and preparation, refer to:

[`dataset.md`](dataset.md)

---

## Annotations

The label files are standard YOLO OBB annotation `.txt` files exported from CVAT.

The annotation workflow used in this project was:

1. Annotate SDSS images using CVAT
2. Export annotations in YOLO OBB format
3. Organize labels alongside corresponding images

You may create your own dataset splits or annotations if desired, provided the directory structure remains compatible with YOLO training.

---

## Training Command

Run training using:

```bash
python src/train/train.py --config configs/train/finalModel.yaml
```

Training outputs, weights/ checkpoints, and validation metrics are automatically saved under:

```text
runs/finalModel/
```

---

## Training Configuration

- Baseline model configuration: [`baselineModel.yaml`](../configs/train/baselineModel.yaml)
- Final model configuration: [`finalModel.yaml`](../configs/train/finalModel.yaml)
---

## Dataset YAML

The YOLO dataset definition file specifies dataset paths and class mappings:

- Baseline model configuration: [`baselineModel.yaml`](../configs/train/yolo11n.yaml)
- Final model configuration: [`finalModel.yaml`](../configs/train/yolo11x-obb.yaml)

---

## Model Selection

The base YOLO model can be changed directly in the training configuration:

```yaml
model:
  weights: yolo11x-obb.pt
```

Other YOLO variants such as:

* `yolo11n-obb.pt`
* `yolo11s-obb.pt`
* `yolo11m-obb.pt`
* `yolo11l-obb.pt`

can also be used depending on available compute resources and desired performance.

---

## Notes

* GPU training is strongly recommended for large-scale experiments.
* Multi-GPU training can be enabled by setting:

```yaml
device: "0,1"
```

* Mixed precision (`amp: true`) was used during training in the paper.
* The final model reported in the paper was trained on the Param Shakti HPC facility at IIT Kharagpur.
