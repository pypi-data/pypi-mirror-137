# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the MatrixView class
"""

from __future__ import annotations

from typing import Sequence

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..inv.investigation import Investigation
from .investigator_window_predefined_view import InvestigatorWindowPredefinedView
from .options_histograms import OptionsHistogram
from .options_scatterplot import OptionsScatterplot
from .options_scatterplot_statistics import OptionsScatterplotStatistics

class MatrixView(InvestigatorWindowPredefinedView, OptionsHistogram, OptionsScatterplot, OptionsScatterplotStatistics):
    """A class representing a MatrixView

    The view defines how a matrix plot should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """

    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "Matrix")

    def copy(self):
        """Create a copy of this view

        Returns:
            MatrixView: the copied view
        """
        copy = MatrixView(None)
        copy._investigation = self._investigation
        copy._plot_type = self._plot_type
        copy._options = self._options
        copy._data.CopyFrom(self._data)
        copy._dataset_priority_order = list(self._dataset_priority_order)
        return copy

    ######################################################################
    # Display by data settings
    ######################################################################

    def set_dimensions(self, dimension_names: Sequence[str]):
        """Sets the dimensions to be shown in the matrix plot

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

        ids = [super(MatrixView, self)._get_continuous_id(name) for name in dimension_names]
        del self._data.display_by_data.selected_dimensions[:]
        self._data.display_by_data.selected_dimensions.extend(ids)

    ######################################################################
    # Histogram settings
    ######################################################################

    def show_histograms(self, show: bool):
        """Set whether the histograms should be shown in the matrix plot diagonal

        Args:
            show (bool): Should the histograms be shown
        """
        self._data.histogram_settings.show_histograms = show
