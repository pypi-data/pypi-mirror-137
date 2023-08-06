# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the CrossplotView class
"""

from __future__ import annotations

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..inv.investigation import Investigation
from .investigator_window_predefined_view import InvestigatorWindowPredefinedView
from .options_histograms import OptionsHistogram
from .options_scatterplot import OptionsScatterplot
from .options_scatterplot_statistics import OptionsScatterplotStatistics


class CrossplotView(InvestigatorWindowPredefinedView, OptionsHistogram, OptionsScatterplot, OptionsScatterplotStatistics):
    """A class representing a CrossplotView

    The view defines how a crossplot should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """

    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "Crossplot")

    def copy(self) -> CrossplotView:
        """Create a copy of this view

        Returns:
            CrossplotView: the copied view
        """
        copy = CrossplotView(None)
        copy._investigation = self._investigation
        copy._plot_type = self._plot_type
        copy._options = self._options
        copy._data.CopyFrom(self._data)
        copy._dataset_priority_order = list(self._dataset_priority_order)
        return copy

    ######################################################################
    # Display by data settings
    ######################################################################

    def set_x_dimension(self, dimension: str):
        """Sets the X dimension to be shown in the crossplot

        Args:
            dimension (str): The name of the dimension to be used

        Raises:
            ValueError: if the name is not a valid continuous dimension
        """
        dimension_id = super(CrossplotView, self)._get_continuous_id(dimension)
        self._data.display_by_data.selected_dimension_x = dimension_id

    def set_y_dimension(self, dimension: str):
        """Sets the Y dimension to be shown in the crossplot

        Args:
            dimension (str): The name of the dimension to be used

        Raises:
            ValueError: if the name is not a valid continuous dimension
        """
        dimension_id = super(CrossplotView, self)._get_continuous_id(dimension)
        self._data.display_by_data.selected_dimension_y = dimension_id

    ######################################################################
    # Histogram settings
    ######################################################################

    def show_x_histogram(self, show: bool):
        """Set whether the X histogram should be shown in the crossplot

        Args:
            show (bool): Should this histogam be shown
        """
        self._data.histogram_settings.show_horizontal_histogram = show

    def show_y_histogram(self, show: bool):
        """Set whether the Y histogram should be shown in the crossplot

        Args:
            show (bool): Should the histogam be shown
        """
        self._data.histogram_settings.show_vertical_histogram = show

    def reverse_histograms(self, reverse_orientation: bool):
        """Set whether the histograms should be reversed in the crossplot

        Args:
            reverse_orientation (bool): if True, the base of the histogram will next to the crossplot axis
        """
        self._data.histogram_settings.reverse_histogram_orientation = reverse_orientation
