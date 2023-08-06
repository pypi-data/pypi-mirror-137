# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the InvestigatorWindowPredefinedView class

This class is internal and is only exposed via inheritance
"""

from __future__ import annotations

from typing import Dict, List, Sequence

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..protos import predefined_view_pb2
from .predefined_view import PredefinedView


class OptionsScatterplot(PredefinedView):
    """A class representing a InvestigatorWindowPredefinedView

    The view defines features that are common to multiple different views.
    """

    ######################################################################
    # Display by data settings
    ######################################################################

    def set_appearance_by(self, appearance_by_option: str):
        """Sets what attribute in the investigation is used to determine the appearance of the data in the view

        Args:
            color_by_option (str): The name of the attribute in the investigation

        Raises:
            ValueError: if the appearance_by_option is not valid
        """
        appearance_by_id = self._get_appearance_by_id(appearance_by_option)
        self._data.display_by_data.selected_appearance_by = appearance_by_id

    ######################################################################
    # Data settings
    ######################################################################

    def set_contour_by(self, contour_by_option: str):
        """Sets what discrete attribute in the investigation is used to determine the contours that should be shown in the view

        Args:
            contour_by_option (str): The name of the attribute in the investigation

        Raises:
            ValueError: if the contour_by_option is not valid
        """
        option = next((x.id for x in self._options.data_settings.available_contour_bys if x.name == contour_by_option), None)
        if option is None:
            options = [x.name for x in self._options.data_settings.available_contour_bys]
            raise ValueError(f"contour_by_option must be one of {str(options)}")
        self._data.data_settings.selected_contour_by = option