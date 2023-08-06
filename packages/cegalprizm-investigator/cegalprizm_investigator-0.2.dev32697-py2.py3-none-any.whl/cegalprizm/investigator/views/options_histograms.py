# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the InvestigatorWindowPredefinedView class

This class is internal and is only exposed via inheritance
"""

from __future__ import annotations

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from .predefined_view import PredefinedView

_AVAILABLE_COUNT_AXIS_TYPES = ["count", "percentage", "relative percentage", "proportional"]


class OptionsHistogram(PredefinedView):
    """A class representing a InvestigatorWindowPredefinedView

    The view defines features that are common to multiple different views.
    """

    def set_count_axis(self, count_type: str):
        """Set the what values should be used for the histogram count axis

        Args:
            count_type (str): A string describing what values should be used on the count axis

        Raises:
            ValueError: if count_type is not a valid string
        """
        if count_type not in _AVAILABLE_COUNT_AXIS_TYPES:
            raise ValueError(f"count_type must be one of {str(_AVAILABLE_COUNT_AXIS_TYPES)}")
        self._data.histogram_settings.count_type = count_type

    def show_histogram_as(self, bars_lines: str):
        """Set whether the histogram data should be drawn as bars or lines

        Args:
            bars_lines (str): A string describing how the histogram data should be shown

        Raises:
            ValueError: if bars_lines is not a valid string
        """
        available_bars_lines = ["bars", "lines"]
        if bars_lines not in available_bars_lines:
            raise ValueError(f"bars_lines must be one of {str(available_bars_lines)}")
        self._data.histogram_settings.bars_lines = bars_lines

    def show_stacked_histogram(self, stacked: bool):
        """Set whether the histogram data should be shown as stacked

        Args:
            stacked (bool): Should the histogram be shown stacked
        """
        if stacked:
            self._data.histogram_settings.stacked = "stacked"
        else:
            self._data.histogram_settings.stacked = "unstacked"

    def show_filled_histogram(self, filled: bool):
        """Set whether the histogram data should be shown as filled

        Args:
            filled (bool): Should the histogram be shown filled
        """
        if filled:
            self._data.histogram_settings.filled = "filled"
        else:
            self._data.histogram_settings.filled = "empty"
    