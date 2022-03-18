import re
from typing import List, Iterable
from english_words import english_words_set


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

def rewrap_hyphenated_words(li: list) -> list:
    """
    Reorganise a list of strings so that word fragments separated
    by hyphens or em dashes to start new lines are joined into a single
    word if the word fragments have no meaning by themselves.

    Args:
        li: List of strings/sentences.

    Returns:
        List of strings/sentences with hyphenated words joined into a single word.

    """
    current = None
    for ix, l in enumerate(li):
        regex_match = re.search(r'\w+(-|–){1}$', l)
        if current:
            word_fragment = current.rstrip('-')
            # TODO: Handle non-English words
            if word_fragment in english_words_set:
                li[ix] = word_fragment + l
            else:
                li[ix] = word_fragment + l
            current = None
        if regex_match:
            # Strip matching regex from the end of the string.
            li[ix] = l[:regex_match.start()]
            current = regex_match[0]
    return li