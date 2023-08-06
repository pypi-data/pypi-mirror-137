# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the MapView class
"""

from __future__ import annotations

from typing import List, Sequence, Union

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..inv.investigation import Investigation
from .predefined_view import PredefinedView

_NULL_PROPERTY_ID = "00000000-0000-0000-0000-000000000000"


class MapView(PredefinedView):
    """A class representing a MapView

    The view defines how a map should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """
    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "Map")

    def copy(self):
        """Create a copy of this view

        Returns:
            MapView: the copied view
        """
        copy = MapView(None)
        copy._investigation = self._investigation
        copy._plot_type = self._plot_type
        copy._options = self._options
        copy._data.CopyFrom(self._data)
        copy._dataset_priority_order = list(self._dataset_priority_order)
        return copy

    ######################################################################
    # Multi-Views
    #####################################################################

    def create_property_views(self, property_names: Sequence[str]) -> List[MapView]:
        """Creates a copy of this view for each property specified

        Args:
            property_names (Sequence[str]): A list of the properties to be used

        Returns:
            List[MapView]: a list of views; one per specified property
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

    def create_grid_views(self, grid_names: Sequence[str]) -> List[MapView]:
        """Creates a copy of this view for each grid specified

        Args:
            grid_names (Sequence[str]): A list of the grids to be used

        Returns:
            List[MapView]: a list of views; one per specified grid
        """
        views = []
        for name in grid_names:
            view = self.copy()
            view.set_grid(name)
            views.append((name, view))
        return views

    def create_zone_views(self, zone_names: Sequence[str]) -> List[MapView]:
        """Creates a copy of this view for each zone specified

        Args:
            zone_names (Sequence[str]): A list of the zones to be used

        Returns:
            List[MapView]: a list of views; one per specified zone
        """
        views = []
        for name in zone_names:
            view = self.copy()
            view.set_zone(name)
            views.append((name, view))
        return views

    def create_zone_property_views(self, zone_properties: Sequence[str]) -> List[MapView]:
        """Creates a copy of this view for each zone property specified

        Args:
            zone_properties (Sequence[str]): A list of the zone properties to be used

        Returns:
            List[MapView]: a list of views; one per specified zone property
        """
        views = []
        for name in zone_properties:
            view = self.copy()
            view.set_zone_property(name)
            views.append((name, view))
        return views

    ######################################################################
    # Map settings
    ######################################################################

    def show_depth_property(self):
        """Sets the depth map to be shown
        """
        self._data.map_settings.selected_property = _NULL_PROPERTY_ID

    def set_property(self, property_name: str):
        """Set the property to be shown on the map

        Args:
            property_name (str): The name of the property to be used

        Raises:
            ValueError: if property_name is not valid
        """
        property_id = self.__get_property_id(property_name)
        self._data.map_settings.selected_property = property_id

    def set_grid(self, grid_name: str):
        """Set the grid to be shown on the map

        Args:
            grid_name (str): The name of the grid to be used

        Raises:
            ValueError: if grid_name is not valid
        """
        grid_id = next((x.id for x in self._options.map_settings.available_grids if x.name == grid_name), None)
        if grid_id is None:
            options = [x.name for x in self._options.map_settings.available_grids]
            raise ValueError(f"grid_name must be one of {str(options)}")
        self._data.map_settings.selected_grid = grid_id

    def set_z(self, value: Union[int, float]):
        """Set the z to be displayed on the map

        Args:
            value (Union[int, float]): The z value to be used

        Raises:
            ValueError: if value is not valid
        """
        if value < self._options.map_settings.range_z.min or value > self._options.map_settings.range_z.max:
            raise ValueError(f"value must be between {self._options.map_settings.range_z.min} and {self._options.map_settings.range_z.max}")
        self._data.map_settings.selected_map_type = "z"
        self._data.map_settings.selected_z = value

    def set_k(self, value: int):
        """Set the k layer to be displayed on the map

        Args:
            value (int): The k value to be used

        Raises:
            ValueError: if value is not valid
        """
        if not isinstance(value, int):
            raise ValueError("value must be a int")
        if value < self._options.map_settings.range_k.min or value > self._options.map_settings.range_k.max:
            raise ValueError(f"value must be between {self._options.map_settings.range_k.min} and {self._options.map_settings.range_k.max}")
        self._data.map_settings.selected_map_type = "k"
        self._data.map_settings.selected_k = value

    def set_surface(self, surface_name: str):
        """Set the surface to be shown in the view

        Args:
            surface_name (str): The name of the surface to be used
        """
        surface_id = next((x.id for x in self._options.map_settings.available_surfaces if x.name == surface_name), None)
        if surface_id is None:
            options = [x.name for x in self._options.map_settings.available_surfaces]
            raise ValueError(f"surface_name must be one of {str(options)}")
        self._data.map_settings.selected_map_type = "surface"
        self._data.map_settings.selected_surface = surface_id

    def set_zone_property(self, zone_property: str):
        """Set the zone property to be shown in the view

        Args:
            zone_property (str): The name of the zone property to be used
        """
        if zone_property not in self._options.map_settings.available_zone_property_options:
            options = self._options.map_settings.available_zone_property_options
            raise ValueError(f"zone_property must be one of {str(options)}")
        self._data.map_settings.selected_zone_property = zone_property

    def set_zone(self, zone_name: str):
        """Set the zone to be shown in the view

        Args:
            zone_name (str): The name of the zone to be used
        """
        zone_id = self.__get_zone_id(zone_name)
        self._data.map_settings.selected_map_type = "zone"
        self._data.map_settings.selected_zone = zone_id

    def set_boreholes(self, borehole_names: Sequence[str]):
        """Set the boreholes to be shown in the view

        Args:
            borehole_names (Sequence[str]): The list of borehole to be used
        """
        del self._data.map_settings.selected_boreholes[:]
        for name in borehole_names:
            self._data.map_settings.selected_boreholes.append(self.__get_borehole_id(name))

    def show_boreholes(self, show: bool):
        """Set whether the borehole should be shown on the map

        Args:
            show (bool): Should the borehole be shown
        """
        self._data.map_settings.show_boreholes = show

    def set_interpolate(self, interpolate: bool):
        """Set whether the map data should be interpolated

        Args:
            show (bool): Should the data be interpolated
        """
        self._data.map_settings.interpolate = interpolate

    def show_contours(self, show: bool):
        """Set whether the contours should be shown on the map

        Args:
            show (bool): Should the contours be shown
        """
        self._data.map_settings.show_contours = show

    ######################################################################
    # Private methods
    ######################################################################

    def __get_property_id(self, property_name: str) -> str:
        property_id = next((x.id for x in self._options.map_settings.available_properties if x.name == property_name), None)
        if property_id is None:
            options = [x.name for x in self._options.map_settings.available_properties]
            raise ValueError(f"property_name must be one of {str(options)}")
        return property_id

    def __get_zone_id(self, zone_name: str):
        zone_id = next((x.id for x in self._options.map_settings.available_zones if x.name == zone_name), None)
        if zone_id is None:
            options = [x.name for x in self._options.map_settings.available_zones]
            raise ValueError(f"zone_name must be one of {str(options)}")
        return zone_id

    def __get_borehole_id(self, name: str):
        borehole_id = next((x.id for x in self._options.map_settings.available_boreholes if x.name == name), None)
        if borehole_id is None:
            options = [x.name for x in self._options.map_settings.available_boreholes]
            raise ValueError(f"name must be one of {str(options)}")
        return borehole_id
