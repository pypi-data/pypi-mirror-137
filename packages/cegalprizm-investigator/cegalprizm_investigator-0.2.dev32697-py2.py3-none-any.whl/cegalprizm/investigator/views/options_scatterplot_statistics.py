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


class OptionsScatterplotStatistics(PredefinedView):
    """A class representing a InvestigatorWindowPredefinedView

    The view defines features that are common to multiple different views.
    """

    def set_draw_statistics(self, draw_statistics: bool):
        """Set whether the statistics should be shown

        Args:
            show (bool): Should the statistics be shown
        """
        self._data.statistics_settings.draw_statistics = draw_statistics

    def show_statistics_mean(self, show_mean: bool):
        """Set whether the mean should be shown

        Args:
            show (bool): Should the mean be shown
        """
        self._data.statistics_settings.show_mean = show_mean

    def show_statistics_median(self, show_median: bool):
        """Set whether the median should be shown

        Args:
            show (bool): Should the median be shown
        """
        self._data.statistics_settings.show_median = show_median

    def show_statistics_percentile(self, show_P10_P90: bool):
        """Set whether the P10/P90 percentile values should be shown

        Args:
            show (bool): Should the percentile values be shown
        """
        self._data.statistics_settings.show_P10_P90 = show_P10_P90

    def show_statistics_minmax(self, show_min_max: bool):
        """Set whether the min/max of the statistics should be shown

        Args:
            show (bool): Should the statistics min/max be shown
        """
        self._data.statistics_settings.show_min_max = show_min_max
