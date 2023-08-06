# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the ContinuousDimension class
"""

# pylint: disable=relative-beyond-top-level

from ..protos import investigation_pb2
from ..utils import _get_numeric_precision
from ..utils import _clamp_precision_value


class ContinuousDimension:
    """A class representing a continuous dimension in a Blueback Investigation

    This object provides the API to be used to set/get information about a specific continuous dimension
    """

    def __init__(self, dimension_info: investigation_pb2.ContinuousDimensionInfo):
        self._dimension_info = dimension_info

    def set_name(self, name: str):
        """Set the name to be used for this dimension

        Note: Changes are applied by calling :py:func:Investigation.refresh()

        Args:
            name (str): The name to be used

        Raises:
            ValueError: is name is empty
        """
        if len(name) == 0:
            raise ValueError("name cannot be empty")

        self._dimension_info.name = name

    def set_display_units(self, symbol: str):
        """Set the display unit to be used for this dimension

        Args:
            symbol (str): The display unit to be used

        Raises:
            ValueError: The provided symbol is not valid for this dimension
        """
        if symbol not in self._dimension_info.available_units:
            raise ValueError(f"symbol must be one of {str(self._dimension_info.available_units)}")

        self._dimension_info.display_units = symbol

    def set_precision(self, precision: str, value: int):
        """Set the precisiop format to be used for this dimension

        Args:
            precision (str): The type of precision to be applied ['decimalplaces', 'significantfigures', 'engineering']
            value (int): The precision value to to applied. eg number of decimal places

        Raises:
            ValueError: If the precision string is not a valid option
            ValueError: If the value is not a valid option for the provided precision
        """
        self._dimension_info.precision.precision = _get_numeric_precision(precision)
        self._dimension_info.precision.value = _clamp_precision_value(self._dimension_info.precision.precision, value)

    def set_axis_logarithmic(self, is_logarithmic: bool):
        """Set the dimension to be displayed as logarithmic

        Args:
            is_logarithmic (bool): Whether to display as logarithmic or not
        """
        self._dimension_info.view.is_logarithmic = is_logarithmic

    def set_axis_reversed(self, is_reversed: bool):
        """Set the dimension to be displayed as reversed

        Args:
            is_reversed (bool): Whether to reverse the axis or not
        """
        self._dimension_info.view.is_reversed = is_reversed

    def set_range(self, min_value: float, max_value: float):
        """Set the range to be used for the dimension

        If either value is set to None then the approriate value will be determined from the investigation data

        Args:
            min_value (float): The minimum value to tbe used for the dimension range
            max_value (float): The maximum value to tbe used for the dimension range
        """
        if min_value:
            self._dimension_info.view.range.is_min_manual = True
            self._dimension_info.view.range.manual_extents.min = min_value

        if max_value:
            self._dimension_info.view.range.is_max_manual = True
            self._dimension_info.view.range.manual_extents.max = max_value

    def set_number_of_bins(self, value: int):
        """Set the number of histogram bins into which the dimension range should be split

        Args:
            value (int): The number of bins to be used

        Raises:
            ValueError: If the value is not greater than 0
        """
        if value <= 0:
            raise ValueError("value must be > 0")

        self._dimension_info.view.bins.use_bin_size = False
        self._dimension_info.view.bins.num_bins = value

    def set_bin_size(self, value: float):
        """Set the bin size which should be applied to the dimension range

        Args:
            value (float): The size of the bin to be used

        Raises:
            ValueError: If the value is 0
        """
        if value == 0:
            raise ValueError("value must not be equal to 0")

        self._dimension_info.view.bins.use_bin_size = True
        self._dimension_info.view.bins.bin_size = value
