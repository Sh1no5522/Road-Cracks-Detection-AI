"""Create reproducible train/validation/test splits from VOC image/XML pairs."""
from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")


def find_image(images_dir: Path, stem: str) -> Path | None:
    for extension in IMAGE_EXTENSIONS:
        candidate = images_dir / f"{stem}{extension}"
        if candidate.exists():
            return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Split Pascal VOC image/XML pairs reproducibly.")
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/raw"))
    parser.add_argument("--train", type=float, default=0.70)
    parser.add_argument("--val", type=float, default=0.20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if not 0 < args.train < 1 or not 0 < args.val < 1 or args.train + args.val >= 1:
        raise ValueError("--train and --val must be positive and add up to less than 1.")
    pairs = [(xml, find_image(args.images, xml.stem)) for xml in args.annotations.glob("*.xml")]
    pairs = [(xml, image) for xml, image in pairs if image is not None]
    if not pairs:
        raise FileNotFoundError("No matching XML/image pairs found.")
    random.Random(args.seed).shuffle(pairs)
    train_end = int(len(pairs) * args.train)
    val_end = train_end + int(len(pairs) * args.val)
    split_pairs = {"train": pairs[:train_end], "val": pairs[train_end:val_end], "test": pairs[val_end:]}
    for split, items in split_pairs.items():
        image_dir = args.output / split / "images"
        annotation_dir = args.output / split / "annotations"
        image_dir.mkdir(parents=True, exist_ok=True)
        annotation_dir.mkdir(parents=True, exist_ok=True)
        for xml_path, image_path in items:
            shutil.copy2(xml_path, annotation_dir / xml_path.name)
            shutil.copy2(image_path, image_dir / image_path.name)
        print(f"{split}: {len(items)} pairs")


if __name__ == "__main__":
    main()
