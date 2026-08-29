"""Export a trained PyTorch checkpoint to ONNX."""
from __future__ import annotations

import argparse
from pathlib import Path
from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", required=True)
    parser.add_argument("--format", choices=("onnx", "engine", "openvino"), default="onnx")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--half", action="store_true", help="Use FP16 where supported (typically NVIDIA GPU).")
    args = parser.parse_args()
    if not Path(args.weights).exists():
        raise FileNotFoundError(args.weights)
    artifact = YOLO(args.weights).export(format=args.format, imgsz=args.imgsz, half=args.half, simplify=args.format == "onnx")
    print(f"Exported: {artifact}")


if __name__ == "__main__":
    main()
