"""Run road-defect detection on an image, video, directory, or webcam."""
from __future__ import annotations

import argparse
from pathlib import Path
from ultralytics import YOLO


def parse_source(value: str) -> str | int:
    return int(value) if value.isdigit() else value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", default="models/best.pt")
    parser.add_argument("--source", required=True, help="Image/video path, directory, URL, or webcam index 0")
    parser.add_argument("--conf", type=float, default=0.30)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--project", default="runs/predict")
    parser.add_argument("--name", default="roadvision")
    args = parser.parse_args()
    if not Path(args.weights).exists():
        raise FileNotFoundError(f"Weights not found: {args.weights}. Train first or copy best.pt to models/.")
    YOLO(args.weights).predict(source=parse_source(args.source), conf=args.conf, imgsz=args.imgsz,
                               save=args.save, project=args.project, name=args.name, exist_ok=True)


if __name__ == "__main__":
    main()
