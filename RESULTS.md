# Results

## Configuration

- **Model:** YOLOv11 Nano
- **Dataset:** RDD2022 (Japan + USA only)
- **Training:** 50 epochs, 640×640 images, AdamW, batch=11, seed=42
- **Hardware:** NVIDIA RTX 4050 (6GB VRAM)
- **Duration:** 1.575 hours

## Data Split

- Train: 10,780 images
- Val: 2,254 images
- Test: 2,277 images (held-out evaluation)

## Validation Metrics

| Metric | Value |
|--------|-------|
| Precision | 0.629 |
| Recall | 0.581 |
| mAP@50 | 0.620 |
| mAP@50–95 | 0.307 |
| Inference | 1.9 ms/image |

## Test Set Metrics

| Metric | Value |
|--------|-------|
| Precision | 0.606 |
| Recall | 0.583 |
| mAP@50 | 0.599 |
| mAP@50–95 | 0.299 |
| Inference | 3.5 ms/image |

## Per-Class Performance

| Class | Precision | Recall | mAP@50 |
|-------|-----------|--------|--------|
| Longitudinal crack | 0.612 | 0.604 | 0.621 |
| Transverse crack | 0.516 | 0.405 | 0.416 |
| Alligator crack | 0.637 | 0.570 | 0.618 |
| Pothole | 0.658 | 0.753 | 0.739 |

## Notes

- Test performance matches validation (no overfitting)
- Potholes detected most reliably (0.753 recall)
- Transverse cracks are most challenging (thin vs lane markings)
- Dataset and model weights excluded from Git (too large)
