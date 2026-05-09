# Prediction / Inference

This stage performs inference using a trained YOLOv11 model on SDSS imaging data.

The prediction pipeline generates:

* annotated prediction images
* YOLO-format detection labels
* confidence scores
* candidate detections for downstream analysis

---

## Prerequisites

Before running inference, ensure that:

1. The trained model weights are available
2. The dataset images are downloaded
3. The dataset directory structure is valid

Expected structure:

```text
data/finalModel/test/
└── images/
```

The trained weights are typically stored under:

```text
runs/finalModel/weights/
```

---

## Running Prediction

Run inference using:

```bash
python src/predict/predict.py --config configs/predict/finalModel.yaml
```

---

## Prediction Configuration

- Baseline model configuration: [`baselineModel.yaml`](../configs/predict/baselineModel.yaml)
- Final model configuration: [`finalModel.yaml`](../configs/predict/finalModel.yaml)

---

## Output Structure

Prediction outputs are automatically saved under:

```text
results/finalModel/predictions/
```

Typical structure:

```text
results/finalModel/predictions/
├── labels/
├── image1.jpg
├── image2.jpg
└── ...
```

Where:

* `labels/` contains YOLO-format prediction files
* images contain rendered bounding boxes and detections

---

## Prediction Script

The prediction pipeline is implemented in:  [predict.py](../src/predict/predict.py) 


The script performs the following steps:

1. Load inference configuration
2. Load trained YOLO model weights
3. Scan input image directory
4. Run batched inference
5. Save prediction images and labels
6. Export confidence scores and detections

---

## Important Parameters

### Confidence Threshold

```yaml
conf: 0.55
```

Controls the minimum confidence score required for detections.

Higher values:

* reduce false positives
* produce fewer detections

Lower values:

* increase recall
* may introduce noisy detections

---

### Image Size

```yaml
imgsz: 640
```

Defines the inference image resolution.

Larger image sizes:

* improve small-object detection
* increase inference time and memory usage

---

### Device Selection

```yaml
device: cpu
```

Examples:

```yaml
device: "0"
```

Single GPU inference

```yaml
device: "0,1"
```

Multi-GPU inference

```yaml
device: cpu
```

CPU inference

---

### Batch Size

```yaml
batch: 32
```

Controls the number of images processed simultaneously during inference.

Higher batch sizes:

* improve throughput
* require more GPU memory

---

## Visualization Options

### Show Confidence Scores

```yaml
show_conf: false
```

Controls whether confidence scores are rendered on prediction images.

---

### Show Labels

```yaml
show_labels: false
```

Controls whether class names are displayed on prediction images.

---

### Bounding Box Thickness

```yaml
line_width: 2
```

Defines the rendered bounding box thickness.

---

## Notes

* The prediction pipeline supports both CPU and GPU inference.
* Multi-GPU inference can be enabled directly through the config file.
* YOLO prediction labels are saved automatically for downstream post-processing.
* The outputs from this stage are later used by the filtering and projected separation estimation pipelines.
