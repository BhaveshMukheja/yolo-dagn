import argparse
import yaml
import os
from ultralytics import YOLO


# ---------------------------
# Config Loader
# ---------------------------
def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


# ---------------------------
# Model Loader
# ---------------------------
def load_model(cfg):
    model_path = cfg["model"]["weights"]

    print(f"[INFO] Loading model: {model_path}")
    return YOLO(model_path)


# ---------------------------
# Train Function
# ---------------------------
def train(cfg):
    model = load_model(cfg)

    train_cfg = cfg["train"]

    print("\n[INFO] Starting training...")
    print(f"Project: {train_cfg['project']}")
    print(f"Run name: {train_cfg['name']}")

    results = model.train(
        data=train_cfg["data"],
        epochs=train_cfg["epochs"],
        imgsz=train_cfg["imgsz"],
        batch=train_cfg["batch"],
        device=train_cfg["device"],
        workers=train_cfg["workers"],
        optimizer=train_cfg.get("optimizer", "auto"),
        amp=train_cfg.get("amp", True),
        val=True,
        save=True,
        save_period=train_cfg.get("save_period", -1),
        project=train_cfg["project"],
        name=train_cfg["name"],
        exist_ok=True
    )

    return model, results


# ---------------------------
# Validation
# ---------------------------
def validate(model):
    print("\n[INFO] Running validation...")
    metrics = model.val()
    return metrics


# ---------------------------
# Export Model
# ---------------------------
def export_model(model, cfg):
    export_cfg = cfg.get("export", {})

    if not export_cfg.get("enable", False):
        return

    fmt = export_cfg.get("format", "onnx")

    print(f"\n[INFO] Exporting model to {fmt}...")
    model.export(format=fmt)


# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to training config")
    parser.add_argument("--no_val", action="store_true", help="Skip validation")
    parser.add_argument("--no_export", action="store_true", help="Skip export")

    args = parser.parse_args()

    cfg = load_config(args.config)

    # Ensure output directory exists
    os.makedirs(cfg["train"]["project"], exist_ok=True)

    model, _ = train(cfg)

    if not args.no_val:
        validate(model)

    if not args.no_export:
        export_model(model, cfg)


if __name__ == "__main__":
    main()