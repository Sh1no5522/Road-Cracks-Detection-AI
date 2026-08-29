"""Train a YOLO road-defect detector using Ultralytics."""
from __future__ import annotations

import argparse
from pathlib import Path
from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="config/road_defects.yaml")
    parser.add_argument("--model", default="yolo11n.pt", help="Start small; try yolo11s.pt after baseline.")
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=-1, help="-1 chooses an automatic batch size.")
    parser.add_argument("--device", default=None, help="e.g. 0 for first NVIDIA GPU, cpu for CPU")
    parser.add_argument("--project", default="runs/train")
    parser.add_argument("--name", default="roadvision_baseline")
    args = parser.parse_args()
    if not Path(args.data).exists():
        raise FileNotFoundError(f"Dataset YAML not found: {args.data}")
    model = YOLO(args.model)
    model.train(data=str(Path(args.data).resolve()), epochs=args.epochs, imgsz=args.imgsz, batch=args.batch,
                device=args.device, project=str(Path(args.project).resolve()), name=args.name, exist_ok=True,
                optimizer="AdamW", patience=20, seed=42, hsv_h=0.015, hsv_s=0.5,
                hsv_v=0.3, degrees=5.0, translate=0.05, scale=0.3, mosaic=0.5,
                close_mosaic=10, amp=True)
    print(f"Best checkpoint: {Path(args.project) / args.name / 'weights' / 'best.pt'}")


if __name__ == "__main__":
    main()
