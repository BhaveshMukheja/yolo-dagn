import os
import argparse
import yaml
from ultralytics import YOLO


# ---------------------------
# Load Config
# ---------------------------
def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


# ---------------------------
# Run Inference
# ---------------------------
def run_inference(cfg):
    model_path = cfg["model"]["weights"]
    infer_cfg = cfg["inference"]

    source_dir = infer_cfg["source"]

    # Create output dir
    os.makedirs(infer_cfg["project"], exist_ok=True)

    # Load model
    print(f"\n[INFO] Loading model: {model_path}")
    model = YOLO(model_path)

    # Count images
    image_files = [
        f for f in os.listdir(source_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    print(f"[INFO] Found {len(image_files)} images in {source_dir}")

    # Device
    device = infer_cfg.get("device", "cpu")

    print("\n[INFO] Inference settings:")
    print(f" - Confidence: {infer_cfg['conf']}")
    print(f" - Image size: {infer_cfg['imgsz']}")
    print(f" - Device: {device}")
    print(f" - Batch size: {infer_cfg.get('batch', 16)}")

    # Run inference
    results = model.predict(
        source=source_dir,
        imgsz=infer_cfg["imgsz"],
        conf=infer_cfg["conf"],
        device=device,
        batch=infer_cfg.get("batch", 16),

        save=True,
        save_txt=True,
        save_conf=True,

        line_width=infer_cfg.get("line_width", 2),
        show_conf=infer_cfg.get("show_conf", True),
        show_labels=infer_cfg.get("show_labels", True),

        project=infer_cfg["project"],
        name=infer_cfg["name"],
        exist_ok=True,

        verbose=False
    )

    print("\n[INFO] Inference complete!")
    print(f"[INFO] Results saved to: {infer_cfg['project']}/{infer_cfg['name']}")

    return results

# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to inference config")

    args = parser.parse_args()
    cfg = load_config(args.config)

    run_inference(cfg)


if __name__ == "__main__":
    main()