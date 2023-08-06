# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the ModelIntersectionView class
"""

from __future__ import annotations

from typing import List, Sequence, Union

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..inv.investigation import Investigation
from .predefined_view import PredefinedView


class ModelIntersectionView(PredefinedView):
    """A class representing a ModelIntersectionView

    The view defines how a model intersection should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """

    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "Intersection")

    def copy(self) -> ModelIntersectionView:
        """Create a copy of this view

        Returns:
            ModelIntersectionView: the copied view
        """
        copy = ModelIntersectionView(None)
        copy._investigation = self._investigation
        copy._plot_type = self._plot_type
        copy._options = self._options
        copy._data.CopyFrom(self._data)
        copy._dataset_priority_order = list(self._dataset_priority_order)
        return copy

    ######################################################################
    # Multi-Views
    ######################################################################

    def create_property_views(self, property_names: Sequence[str]) -> List[ModelIntersectionView]:
        """Creates a copy of this view for each property specified

        Args:
            property_names (Sequence[str]): A list of properties to be used

        Returns:
            List[ModelIntersectionView]: a list of views; one per specified property
        """
        if property_names is None:
            raise ValueError("property_names must be defined")
        if len(property_names) == 0:
            raise ValueError("property_names must contain at least 1 entry")

        views = []
        for name in property_names:
            view = self.copy()
            view.set_property(name)
            views.append((name, view))
        return views

    def create_grid_views(self, grid_names: Sequence[str]) -> List[ModelIntersectionView]:
        """Creates a copy of this view for each grid specified

        Args:
            grid_names (Sequence[str]): A list of grid to be used

        Returns:
            List[ModelIntersectionView]: a list of views; one per specified grid
        """
        views = []
        for name in grid_names:
            view = self.copy()
            view.set_grid(name)
            views.append((name, view))
        return views

    ######################################################################
    # Intersection settings
    ######################################################################

    def set_property(self, property_name: str):
        """Sets the property to be shown in the view

        Args:
            property_name (str): The name of the property to be used

        Raises:
            ValueError: if the property_name is not a valid property
        """
        property_id = self.__get_property_id(property_name)
        self._data.intersection_settings.selected_property = property_id

    def set_grid(self, grid: str):
        """Sets the grid to be shown in the view

        Args:
            grid (str): The name of the grid to be used

        Raises:
            ValueError: if the property_name is not a valid property
        """
        option = next((x.id for x in self._options.intersection_settings.available_grids if x.name == grid), None)
        if option is None:
            options = [x.name for x in self._options.intersection_settings.available_grids]
            raise ValueError(f"grid must be one of {str(options)}")
        self._data.intersection_settings.selected_grid = option

    def set_north_south(self, value: Union[float, int]):
        """Set the location of the north-south intersection

        Args:
            value (Union[float, int]): The location of the intersection to be used

        Raises:
            ValueError: if the value is not valid
        """
        if value < self._options.intersection_settings.range_north_south.min or value > self._options.intersection_settings.range_north_south.max:
            raise ValueError(f"value must be between {self._options.intersection_settings.range_north_south.min} and {self._options.intersection_settings.range_north_south.max}")
        self._data.intersection_settings.selected_intersection_type = "ns"
        self._data.intersection_settings.selected_north_south = value

    def set_east_west(self, value: Union[float, int]):
        """Set the location of the east-west intersection

        Args:
            value (Union[float, int]): The location of the intersection to be used

        Raises:
            ValueError: if the value is not valid
        """
        if value < self._options.intersection_settings.range_east_west.min or value > self._options.intersection_settings.range_east_west.max:
            raise ValueError(f"value must be between {self._options.intersection_settings.range_east_west.min} and {self._options.intersection_settings.range_east_west.max}")
        self._data.intersection_settings.selected_intersection_type = "ew"
        self._data.intersection_settings.selected_east_west = value

    def set_i(self, value: int):
        """Set the i slice to show

        Args:
            value (int): The i slice index to be used

        Raises:
            ValueError: if the value is not valid
        """
        if value < self._options.intersection_settings.range_i.min or value > self._options.intersection_settings.range_i.max:
            raise ValueError(f"value must be between {self._options.intersection_settings.range_i.min} and {self._options.intersection_settings.range_i.max}")
        self._data.intersection_settings.selected_intersection_type = "i"
        self._data.intersection_settings.selected_i = value

    def set_j(self, value: int):
        """Set the j slice to show

        Args:
            value (int): The j slice index to be used

        Raises:
            ValueError: if the value is not valid
        """
        if value < self._options.intersection_settings.range_j.min or value > self._options.intersection_settings.range_j.max:
            raise ValueError(f"value must be between {self._options.intersection_settings.range_j.min} and {self._options.intersection_settings.range_j.max}")
        self._data.intersection_settings.selected_intersection_type = "j"
        self._data.intersection_settings.selected_j = value

    def set_borehole(self, borehole_name: str):
        """Sets the borhole for which the intersection should be shown

        Args:
            borehole (str): The borehole name

        Raises:
            ValueError: if the breohole is not valid
        """
        borehole_id = self.__get_borehole_id(borehole_name)
        self._data.intersection_settings.selected_intersection_type = "borehole"
        self._data.intersection_settings.selected_borehole = borehole_id

    ######################################################################
    # Private methods
    ######################################################################

    def __get_property_id(self, property_name: str) -> str:
        property_id = next((x.id for x in self._options.intersection_settings.available_properties if x.name == property_name), None)
        if property_id is None:
            options = [x.name for x in self._options.intersection_settings.available_properties]
            raise ValueError(f"property_name must be one of {str(options)}")
        return property_id

    def __get_borehole_id(self, name: str):
        borehole_id = next((x.id for x in self._options.intersection_settings.available_boreholes if x.name == name), None)
        if borehole_id is None:
            options = [x.name for x in self._options.intersection_settings.available_boreholes]
            raise ValueError(f"name must be one of {str(options)}")
        return borehole_id
