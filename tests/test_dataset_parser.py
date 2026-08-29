import pytest
from src.dataset_parser import convert_voc_to_yolo_bbox


def test_converts_voc_box_to_normalized_yolo_box():
    x, y, width, height = convert_voc_to_yolo_bbox((1000, 1000), (100, 200, 500, 600))
    assert x == pytest.approx(0.3)
    assert y == pytest.approx(0.4)
    assert width == pytest.approx(0.4)
    assert height == pytest.approx(0.4)


def test_clips_box_at_image_boundary():
    x, y, width, height = convert_voc_to_yolo_bbox((100, 100), (-5, 10, 120, 90))
    assert (x, y, width, height) == pytest.approx((0.5, 0.5, 1.0, 0.8))


def test_rejects_empty_box():
    with pytest.raises(ValueError):
        convert_voc_to_yolo_bbox((100, 100), (50, 10, 50, 90))
