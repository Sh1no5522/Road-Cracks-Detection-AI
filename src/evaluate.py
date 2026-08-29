"""Evaluate a trained model on the configured validation or test split."""
from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", required=True)
    parser.add_argument("--data", default="config/road_defects.yaml")
    parser.add_argument("--split", choices=("val", "test"), default="test")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--device", default="0")
    parser.add_argument("--project", default="runs/evaluate")
    parser.add_argument("--name", default="japan_usa_test")
    args = parser.parse_args()
    if not Path(args.weights).is_file():
        raise FileNotFoundError(f"Weights not found: {args.weights}")
    YOLO(args.weights).val(data=str(Path(args.data).resolve()), split=args.split, imgsz=args.imgsz,
                           device=args.device, project=str(Path(args.project).resolve()),
                           name=args.name, exist_ok=True, plots=True)


if __name__ == "__main__":
    main()
