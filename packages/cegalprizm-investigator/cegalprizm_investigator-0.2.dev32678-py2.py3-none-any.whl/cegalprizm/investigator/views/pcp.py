# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the ParallelCoordinatesView class
"""

from __future__ import annotations

from typing import Sequence

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..inv.investigation import Investigation
from .investigator_window_predefined_view import InvestigatorWindowPredefinedView


class ParallelCoordinatesView(InvestigatorWindowPredefinedView):
    """A class representing a ParallelCoordinatesView

    The view defines how a parallel coordinates plot should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """

    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "PCP")

    def copy(self):
        """Create a copy of this view

        Returns:
            ParallelCoordinatesView: the copied view
        """
        copy = ParallelCoordinatesView(None)
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
        """Sets the dimensions to be shown in the parallel coordinates plot

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

        ids = [super(ParallelCoordinatesView, self)._get_continuous_id(name) for name in dimension_names]
        del self._data.display_by_data.selected_dimensions[:]
        self._data.display_by_data.selected_dimensions.extend(ids)
