"""Utility functions."""

from typing import List


def paginate_list(_list: list, page_size: int) -> List[list]:
    """Split a list into sublists of size page_size. If the list length isn't a multiple of page_size, the last sublist will be smaller.

    Args:
        _list (list): input list
        page_size (int): size of sublists to return.

    Returns:
        List[list]: A list of sublists.
    """
    return [_list[i : i + page_size] for i in range(0, len(_list), page_size)]
