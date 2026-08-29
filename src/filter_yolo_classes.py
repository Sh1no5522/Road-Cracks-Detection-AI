"""Keep selected YOLO classes while preserving all images and valid boxes."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove unwanted class IDs from YOLO label files in place.")
    parser.add_argument("--labels", type=Path, default=Path("data/processed/labels"))
    parser.add_argument("--keep", type=int, nargs="+", default=[0, 1, 2, 3])
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files.")
    args = parser.parse_args()
    allowed = set(args.keep)
    changed_files = removed_boxes = kept_boxes = 0
    for label_path in args.labels.rglob("*.txt"):
        lines = label_path.read_text(encoding="utf-8").splitlines()
        retained: list[str] = []
        for line in lines:
            fields = line.split()
            if not fields:
                continue
            try:
                class_id = int(fields[0])
            except ValueError as error:
                raise ValueError(f"Invalid class ID in {label_path}: {line!r}") from error
            if class_id in allowed:
                retained.append(line)
                kept_boxes += 1
            else:
                removed_boxes += 1
        if len(retained) != len(lines):
            changed_files += 1
            if not args.dry_run:
                label_path.write_text("\n".join(retained) + ("\n" if retained else ""), encoding="utf-8")
    cleared_caches = 0
    if changed_files and not args.dry_run:
        for cache_path in args.labels.glob("*.cache"):
            cache_path.unlink()
            cleared_caches += 1
    action = "Would update" if args.dry_run else "Updated"
    print(f"{action} {changed_files} label files; kept {kept_boxes} boxes and removed {removed_boxes} boxes. Allowed IDs: {sorted(allowed)}. Cleared {cleared_caches} label caches.")


if __name__ == "__main__":
    main()
