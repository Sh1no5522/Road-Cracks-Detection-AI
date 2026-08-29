"""Convert Pascal VOC road-defect annotations into YOLO detection labels."""
from __future__ import annotations

import argparse
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

CLASS_MAPPING = {"D00": 0, "D10": 1, "D20": 2, "D40": 3}
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")


def convert_voc_to_yolo_bbox(image_size: tuple[int, int], box: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """Convert VOC (xmin, ymin, xmax, ymax) pixels to normalized YOLO xywh."""
    image_width, image_height = image_size
    if image_width <= 0 or image_height <= 0:
        raise ValueError("Image width and height must be positive.")
    xmin, ymin, xmax, ymax = box
    xmin, xmax = sorted((min(float(image_width), max(0.0, xmin)), min(float(image_width), max(0.0, xmax))))
    ymin, ymax = sorted((min(float(image_height), max(0.0, ymin)), min(float(image_height), max(0.0, ymax))))
    if xmax <= xmin or ymax <= ymin:
        raise ValueError(f"Invalid or empty bounding box: {box}")
    x_center = ((xmin + xmax) / 2) / image_width
    y_center = ((ymin + ymax) / 2) / image_height
    width = (xmax - xmin) / image_width
    height = (ymax - ymin) / image_height
    return tuple(max(0.0, min(1.0, value)) for value in (x_center, y_center, width, height))


def parse_xml_annotation(xml_path: Path, label_path: Path) -> int:
    """Write one YOLO label file. Returns the number of kept boxes."""
    root = ET.parse(xml_path).getroot()
    size = root.find("size")
    if size is None:
        raise ValueError(f"Missing <size> in {xml_path}")
    width = int(size.findtext("width", "0"))
    height = int(size.findtext("height", "0"))
    labels: list[str] = []
    for obj in root.findall("object"):
        class_id = CLASS_MAPPING.get(obj.findtext("name", "").strip())
        box = obj.find("bndbox")
        if class_id is None or box is None:
            continue
        values = tuple(float(box.findtext(key, "0")) for key in ("xmin", "ymin", "xmax", "ymax"))
        try:
            x, y, w, h = convert_voc_to_yolo_bbox((width, height), values)
        except ValueError:
            continue
        labels.append(f"{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
    label_path.parent.mkdir(parents=True, exist_ok=True)
    label_path.write_text("\n".join(labels) + ("\n" if labels else ""), encoding="utf-8")
    return len(labels)


def find_image(images_dir: Path, stem: str) -> Path | None:
    for extension in IMAGE_EXTENSIONS:
        candidate = images_dir / f"{stem}{extension}"
        if candidate.exists():
            return candidate
    return None


def convert_split(annotations_dir: Path, images_dir: Path, output_root: Path, split: str) -> None:
    """Convert XML annotations and copy matching images into one YOLO split."""
    image_output = output_root / "images" / split
    label_output = output_root / "labels" / split
    converted = skipped = boxes = 0
    for xml_path in sorted(annotations_dir.glob("*.xml")):
        image_path = find_image(images_dir, xml_path.stem)
        if image_path is None:
            skipped += 1
            continue
        boxes += parse_xml_annotation(xml_path, label_output / f"{xml_path.stem}.txt")
        image_output.mkdir(parents=True, exist_ok=True)
        shutil.copy2(image_path, image_output / image_path.name)
        converted += 1
    print(f"{split}: {converted} images, {boxes} boxes, {skipped} XML files without matching images")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a VOC split to YOLO format.")
    parser.add_argument("--annotations", type=Path, required=True, help="Directory containing VOC XML files")
    parser.add_argument("--images", type=Path, required=True, help="Directory containing matching images")
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    parser.add_argument("--split", choices=("train", "val", "test"), required=True)
    args = parser.parse_args()
    convert_split(args.annotations, args.images, args.output, args.split)


if __name__ == "__main__":
    main()
