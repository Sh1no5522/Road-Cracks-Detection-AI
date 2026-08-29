"""Copy selected country prefixes from an already YOLO-formatted RDD split."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Select country subsets from RDD_SPLIT without changing YOLO labels.")
    parser.add_argument("--source", type=Path, required=True, help="Folder containing train/, val/, and test/")
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    parser.add_argument("--countries", nargs="+", default=["Japan", "United_States"],
                        help="Filename prefixes to retain, e.g. Japan United_States")
    args = parser.parse_args()

    prefixes = tuple(f"{country}_" for country in args.countries)
    total_images = total_missing_labels = 0
    for split in ("train", "val", "test"):
        image_source = args.source / split / "images"
        label_source = args.source / split / "labels"
        if not image_source.is_dir() or not label_source.is_dir():
            raise FileNotFoundError(f"Expected images and labels under: {args.source / split}")
        image_target = args.output / "images" / split
        label_target = args.output / "labels" / split
        image_target.mkdir(parents=True, exist_ok=True)
        label_target.mkdir(parents=True, exist_ok=True)
        kept = missing_labels = 0
        for image_path in image_source.iterdir():
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS or not image_path.name.startswith(prefixes):
                continue
            label_path = label_source / f"{image_path.stem}.txt"
            if not label_path.exists():
                missing_labels += 1
                continue
            shutil.copy2(image_path, image_target / image_path.name)
            shutil.copy2(label_path, label_target / label_path.name)
            kept += 1
        print(f"{split}: copied {kept} image/label pairs; skipped {missing_labels} images without labels")
        total_images += kept
        total_missing_labels += missing_labels
    print(f"Done: {total_images} pairs selected for {', '.join(args.countries)}; {total_missing_labels} skipped.")


if __name__ == "__main__":
    main()
