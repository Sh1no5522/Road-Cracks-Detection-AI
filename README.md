# RoadVision-YOLO

YOLO11n detector for road surface defects (cracks, potholes). Trained on RDD2022 dataset (Japan + USA, 13,311 images). 

**Test Results:** mAP@50: 0.599 | Precision: 0.606 | Recall: 0.583 | Inference: 3.5ms/image

## Setup

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
```

Requires Python 3.10+. For GPU: install CUDA-compatible PyTorch.

## Quick Start

**Prepare dataset:**
```powershell
python -m src.split_dataset --images data/source/images --annotations data/source/annotations --output data/raw --seed 42
python -m src.dataset_parser --annotations data/raw/train/annotations --images data/raw/train/images --split train
```

**Train:**
```powershell
python -m src.train --data config/road_defects.yaml --epochs 50 --device 0
```

**Test:**
```powershell
python -m src.inference --weights models/best.pt --source image.jpg --conf 0.30 --save
```

**Demo (Streamlit):**
```powershell
streamlit run app.py
```

## Results

See [RESULTS.md](RESULTS.md) for detailed metrics by class.

## Dataset

RDD2022 (Road Damage Detection): Japan + United States. Train/Val/Test: 10,780 / 2,254 / 2,277 images.

Classes: longitudinal_crack, transverse_crack, alligator_crack, pothole

```powershell
python -m src.evaluate --weights runs/train/japan_usa_four_class_clean/weights/best.pt --data config/road_defects.yaml --split test --device 0
```

The report and plots are saved under `runs/evaluate/japan_usa_test/`.

## 5. Run the demo

```powershell
Copy-Item runs\train\roadvision_baseline\weights\best.pt models\best.pt
streamlit run app.py
```

## 6. Export

Export ONNX after validating the `.pt` model:

```powershell
python -m src.export --weights runs/train/roadvision_baseline/weights/best.pt --format onnx
```

TensorRT export requires a compatible NVIDIA GPU, CUDA, and TensorRT installation:

```powershell
python -m src.export --weights runs/train/roadvision_baseline/weights/best.pt --format engine --half
```

## Responsible use

This is a decision-support prototype, not a safety-certified road inspection system. Verify detections manually and do not use it as the sole basis for maintenance or safety decisions.

## Dataset attribution

This project uses a locally filtered, YOLO-formatted copy of the Japan and United States portions of RDD2022. Drone and Motorbike images were excluded. Do not commit dataset images or labels to GitHub; follow the source dataset licence and provide attribution when sharing results.

Arya, D. et al. (2024). *RDD2022: A multi-national image dataset for automatic road damage detection*. Geoscience Data Journal. https://doi.org/10.1002/gdj3.260
