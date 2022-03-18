from typing import List, Iterable


def minimal_bounding_box(coords: List[Iterable]) -> list:
    """
    Return the minimally enclosing bounding box of bounding boxes.

    Args:
        coords: A list of coordinates for each bounding box formatted [x1,y1,x2,y2] with the top left as the origin.

    Returns:
        A list of coordinates for the minimally enclosing bounding box for all input bounding boxes.

    """
    x_min = min(coord[0] for coord in coords)
    y_min = min(coord[1] for coord in coords)
    x_max = max(coord[2] for coord in coords)
    y_max = max(coord[3] for coord in coords)
    return [x_min, y_min, x_max, y_max]