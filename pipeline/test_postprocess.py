import postprocess
import unittest
import pytest


def test_minimal_bounding_box():
    # Test case where the second bounding box is below the first and is wider than it.
    bbox_1 = [1, 1, 5, 3]
    bbox_2 = [0.5, 6, 4, 8]
    bboxes = [bbox_1, bbox_2]
    expected_bbox = [0.5, 1, 5, 8]
    assert postprocess.minimal_bounding_box(bboxes) == expected_bbox
