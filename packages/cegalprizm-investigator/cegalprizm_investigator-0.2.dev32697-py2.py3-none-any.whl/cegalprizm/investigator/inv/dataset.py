# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the Dataset class
"""

from typing import Union

import ctypes

# pylint: disable=relative-beyond-top-level

from ..protos import investigation_pb2
from ..utils import _get_shape, _clamp_size, _color_name_to_int


class Dataset:
    """A class representing a dataset in a Blueback Investigation

    This object provides the API to be used to set/get information about a specific dataset
    """

    def __init__(self, dataset_info: investigation_pb2.Dataset):
        self._dataset_info = dataset_info

    def set_name(self, name: str):
        """Set the name to be used for this dataset

        Args:
            name (str): The name to be used

        Raises:
            ValueError: if name is empty
        """
        if len(name) == 0:
            raise ValueError("name cannot be empty")

        self._dataset_info.name = name

    def set_color(self, color: Union[int, str]):
        """Set the color to be used for this dataset

        Args:
            color (Union[int, str]): Either the int value or the matplotlib colorname to be used for the dataset color

        Raises:
            ValueError: if color is not an int or a recognised matplotlib colorname
        """
        if isinstance(color, int):
            col = color
        elif isinstance(color, str):
            col = _color_name_to_int(color)
        else:
            raise ValueError("color must be int or str")

        self._dataset_info.color = ctypes.c_int32(col).value

    def set_shape(self, shape: str, size: int):
        """Set the shape to be used for this dataset

        Args:
            shape (str): The name of the shape to be used
            size (int): The size of the shape to be used

        Raises:
            ValueError: If the shape string is not a valid option
            ValueError: If the size is not a valid option
        """
        self._dataset_info.style.shape = _get_shape(shape)
        self._dataset_info.style.shape_size = _clamp_size(size)

    def set_use_parent(self, color_from_parent: bool):
        """Set whether the dataset should show all children datasets like this dataset

        Args:
            color_from_parent (bool): Whether to use this dataset for all children
        """
        self._dataset_info.style.color_from_parent = color_from_parent
