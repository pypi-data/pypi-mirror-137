# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the HistogramView class
"""

from __future__ import annotations

from typing import List, Sequence

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..inv.investigation import Investigation
from .investigator_window_predefined_view import InvestigatorWindowPredefinedView
from .options_histograms import OptionsHistogram

class HistogramView(InvestigatorWindowPredefinedView, OptionsHistogram):
    """A class representing a HistogramView

    The view defines how a histogram should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """

    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "Histogram")

    def copy(self) -> HistogramView:
        """Create a copy of this view

        Returns:
            HistogramView: the copied view
        """
        copy = HistogramView(None)
        copy._investigation = self._investigation
        copy._plot_type = self._plot_type
        copy._options = self._options
        copy._data.CopyFrom(self._data)
        copy._dataset_priority_order = list(self._dataset_priority_order)
        return copy

    ######################################################################
    # Multi-Views
    ######################################################################

    def create_dimension_views(self, dimensions: Sequence[str]) -> List[HistogramView]:
        """Creates a copy of this view for each dimension specified

        Args:
            dimensions (Sequence[str]): A list of continuous dimensions to be used

        Returns:
            List[HistogramView]: a list of views; one per specified dimension
        """
        views = []
        labels = []
        for name in dimensions:
            view = self.copy()
            view.set_dimension(name)
            views.append(view)
            labels.append(name)
        return views

    ######################################################################
    # General settings
    ######################################################################

    def swap_axes(self):
        """Toggle whether the axes should be swapped in the view
        """
        self._data.general_settings.swap_axes = not self._data.general_settings.swap_axes

    ######################################################################
    # Display by data settings
    ######################################################################

    def set_dimension(self, dimension: str):
        """Sets the dimension to be shown in the histogram

        Args:
            dimension (str): The name of the dimension to be used

        Raises:
            ValueError: if the dimension is not a valid continuous dimension
        """
        dimension_id = super(HistogramView, self)._get_continuous_id(dimension)
        self._data.display_by_data.selected_dimension_x = dimension_id

    def show_multi_histograms(self, show: bool):
        """Set whether the histogram should be shown as a multi-dimension histogram

        Args:
            show (bool): Should the multi-dimension histogram be shown
        """
        self._data.histogram_settings.show_multi_histograms = show

    def set_dimensions(self, dimension_names: Sequence[str]):
        """Sets the dimensions to be shown in the multi histogram

        Args:
            dimension_names (Sequence[str]): A list of the names of the dimensions to be used

        Raises:
            ValueError: if the dimension is not a valid continuous dimension
        """
        if dimension_names is None:
            raise ValueError("dimension_names must be defined")
        if not isinstance(dimension_names, list):
            raise ValueError("dimension_names must be a list of strings")
        if len(dimension_names) == 0:
            raise ValueError("dimension_names must contain at least 1 entry")
        for name in dimension_names:
            if name not in self._investigation.continuous_dimension_names:
                raise ValueError(f"dimension_names list should only contain {str(self._investigation.continuous_dimension_names)}")

        dimension_ids = [super(HistogramView, self)._get_continuous_id(name) for name in dimension_names]
        del self._data.display_by_data.selected_dimensions[:]
        self._data.histogram_settings.show_multi_histograms = True
        self._data.display_by_data.selected_dimensions.extend(dimension_ids)

    def set_barchart(self, barchart_option: str):
        """Set the bar chart option to be displayed

        Args:
            barchart_option (str): The name of the discrete dimension to be used

        Raises:
            ValueError: if the discrete dimension is not valid in the investigation
        """
        option = next((x.id for x in self._options.histogram_settings.available_barchart_options if x.name == barchart_option), None)
        if option is None:
            options = [x.name for x in self._options.histogram_settings.available_barchart_options]
            raise ValueError(f"barchart_option must be one of {str(options)}")
        self._data.histogram_settings.selected_barchart_option = option

    def apply_weighting(self, apply_weighting: bool):
        """Set whether to apply weighting to the histogram values

        Args:
            apply_weighting (bool): If True then weighting will be applied to the histogram
        """
        self._data.histogram_settings.apply_weighting = apply_weighting

    ######################################################################
    # Statistics
    ######################################################################

    def set_draw_statistics(self, draw_statistics: bool):
        """Set whether the statistics should be shown

        Args:
            show (bool): Should the statistics be shown
        """
        self._data.statistics_settings.draw_statistics = draw_statistics
