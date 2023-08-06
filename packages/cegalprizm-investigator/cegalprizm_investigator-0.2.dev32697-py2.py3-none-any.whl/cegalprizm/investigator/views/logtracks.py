# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the LogTracksView class
"""

from __future__ import annotations

from typing import Sequence

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..inv.investigation import Investigation
from .predefined_view import PredefinedView

_AVAILABLE_GROUPINGS = ["well", "property"]

class LogTracksView(PredefinedView):
    """A class representing a LogTracksView

    The view defines how log tracks should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """

    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "LogTracks")

    def copy(self):
        """Create a copy of this view

        Returns:
            LogTracksView: the copied view
        """
        copy = LogTracksView(None)
        copy._investigation = self._investigation
        copy._plot_type = self._plot_type
        copy._options = self._options
        copy._data.CopyFrom(self._data)
        copy._dataset_priority_order = list(self._dataset_priority_order)
        return copy

    ######################################################################
    # Log track settings
    ######################################################################

    def set_boreholes(self, borehole_names: Sequence[str]):
        """Set the boreholes to be shown in the view

        Args:
            borehole_names (Sequence[str]): The names of the boreholes to be used

        Raises:
            ValueError: if the borehole_names is not a valid
        """
        if borehole_names is None:
            raise ValueError("borehole_names must be defined")
        if not isinstance(borehole_names, list):
            raise ValueError("borehole_names must be a list of strings")
        if len(borehole_names) == 0:
            raise ValueError("borehole_names must contain at least 1 entry")

        del self._data.log_tracks_settings.selected_boreholes[:]
        for name in borehole_names:
            self._data.log_tracks_settings.selected_boreholes.append(self.__get_borehole_id(name))

    def set_grids(self, grid_names: Sequence[str]):
        """Set the grids to be shown in the view

        Args:
            grid_names (Sequence[str]): The names of the grids to be used

        Raises:
            ValueError: if the grid_names is not a valid
        """
        if grid_names is None:
            raise ValueError("grid_names must be defined")
        if not isinstance(grid_names, list):
            raise ValueError("grid_names must be a list of strings")
        if len(grid_names) == 0:
            raise ValueError("grid_names must contain at least 1 entry")

        del self._data.log_tracks_settings.selected_grids[:]
        for name in grid_names:
            self._data.log_tracks_settings.selected_grids.append(self.__get_grid_id(name))
            
    def set_properties(self, property_names: Sequence[str]):
        """Set the properties to be shown in the view

        Args:
            property_names (Sequence[str]): The names of the properties to be used

        Raises:
            ValueError: if the grid_names is not a valid
        """
        if property_names is None:
            raise ValueError("property_names must be defined")
        if not isinstance(property_names, list):
            raise ValueError("property_names must be a list of strings")
        if len(property_names) == 0:
            raise ValueError("property_names must contain at least 1 entry")

        del self._data.log_tracks_settings.selected_properties[:]
        for name in property_names:
            self._data.log_tracks_settings.selected_properties.append(self.__get_property_id(name))

    def group_tracks_by(self, grouping: str):
        """Set whether the tracks should be grouped by well or by property

        Args:
            grouping (str): A string describing how the log tracks should be shown

        Raises:
            ValueError: if grouping is not a valid string
        """
        if grouping not in _AVAILABLE_GROUPINGS:
            raise ValueError(f"grouping must be one of {str(_AVAILABLE_GROUPINGS)}")
        self._data.log_tracks_settings.group_tracks_by = grouping

    def show_continuous_fill(self, show: bool):
        """Set whether the continuous tracks should be shown with a continuous fill

        Args:
            show (bool): Should the continuous fill be shown
        """
        self._data.log_tracks_settings.use_continuous_log_fill = show

    ######################################################################
    # Private methods
    ######################################################################

    def __get_property_id(self, name: str):
        option_id = next((x.id for x in self._options.log_tracks_settings.available_properties if x.name == name), None)
        if option_id is None:
            options = [x.name for x in self._options.log_tracks_settings.available_properties]
            raise ValueError(f"name must be one of {str(options)}")
        return option_id

    def __get_borehole_id(self, name: str):
        option_id = next((x.id for x in self._options.log_tracks_settings.available_boreholes if x.name == name), None)
        if option_id is None:
            options = [x.name for x in self._options.log_tracks_settings.available_boreholes]
            raise ValueError(f"name must be one of {str(options)}")
        return option_id

    def __get_grid_id(self, name: str):
        option_id = next((x.id for x in self._options.log_tracks_settings.available_grids if x.name == name), None)
        if option_id is None:
            options = [x.name for x in self._options.log_tracks_settings.available_grids]
            raise ValueError(f"name must be one of {str(options)}")
        return option_id
