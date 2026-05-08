#!/bin/bash
#SBATCH --job-name=yolo11_obb_training
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=48:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# ==========================================================
# Example SLURM Script for YOLOv11x-OBB Training
# ==========================================================
#
# This script was used for multi-GPU training on an HPC cluster.
#
# Notes:
# - Modify paths according to your environment.
# - Adjust GPU count, memory, and batch size
#   depending on available resources.
# - CUDA / module names may differ across clusters.
#
# ==========================================================

# ----------------------------------------------------------
# Load Environment
# ----------------------------------------------------------

module purge
module load compiler/cuda/11.7

# ----------------------------------------------------------
# Activate Conda Environment
# ----------------------------------------------------------

source ~/miniconda3/bin/activate

conda activate yolo11

# ----------------------------------------------------------
# Debug Information
# ----------------------------------------------------------

echo "====================================="
echo "GPU Information"
echo "====================================="

nvidia-smi

echo "====================================="

# ----------------------------------------------------------
# Launch YOLOv11x-OBB Training
# ----------------------------------------------------------

python -c "

from ultralytics import YOLO

# ------------------------------------------------------
# Load Pretrained Model
# ------------------------------------------------------

model = YOLO(
    '/path/to/yolo11x-obb.pt'
)

# ------------------------------------------------------
# Start Training
# ------------------------------------------------------

model.train(

    # Dataset configuration
    data='/path/to/config.yaml',

    # Training configuration
    epochs=300,
    imgsz=1280,
    batch=64,

    # Multi-GPU setup
    device='0,1',

    # Data loading
    workers=16,

    # Optimization
    optimizer='AdamW',
    amp=True,

    # Validation and checkpointing
    val=True,
    save=True,
    save_period=10,

    # Output directory
    project='/path/to/output/runs',

    # Experiment name
    name='yolo11x_obb_multi_gpu'
)

"