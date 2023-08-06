# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the InvestigatorConnection class
"""

from typing import Dict, List, Sequence

import pandas as pd

from cegalprizm.hub import BaseContext, ConnectionParameters

# pylint: disable=relative-beyond-top-level

from .hub_context import InvPyHubContext
from .named_tuples import ContinuousDimensionInfoTuple, InvestigationInfoTuple
from .from_dataframe import _from_dataframe
from .investigations import _available_investigations, _remove_investigation
from .iris import _create_iris_investigation

from .inv.investigation import Investigation

class InvestigatorConnection:
    """This class represents a connection to an instance of Investigator

    The connection to Investigator will be made using Hub. It may be either
        - local (on the same machine running Python)
        - remote (on a machine on the same network)
        - cloud (on a machine connected via the cloud)

    The Investigator may be running as:
        - A plugin inside Petrel
        - A standalone investigator server
    """

    def __init__(self, hub_context: BaseContext = None, hub_connection_parameters: ConnectionParameters = None):
        self._hub_context = InvPyHubContext(hub_context, hub_connection_parameters)

    def renew_context(self):
        """This will force the Hub connection to be reset

        This should only be necessary if Hub is restarted or a new instance of Petrel is attached.
        """
        self._hub_context.force_new()

    def set_connector_labels(self, labels: Dict[str, str]):
        """Set specific connector labels to be used

        The supplied connector labels will be used as a filter to select the connector to be used for communication with Investigator.
        For example, labels can be used to target a specific Petrel instance when more than 1 instance available.

        Args:
            labels (Dict[str, str]): A dictionary of key-value strings labels
        """
        self._hub_context.set_connector_labels(labels)

    def available_investigations(self) -> List[InvestigationInfoTuple]:
        """Returns a list of the available investigations

        Raises:
            CegalHubError: if an unexpected error is reported by Hub

        Returns:
            List[InvestigationInfoTuple]: A list of tuples containing the id and name for each available investigation
        """
        return _available_investigations(self._hub_context)

    def create_iris_investigation(self) -> Investigation:
        """Creates a investigation containing the iris dataset

        THe iris dataset is well know in data science and often used for examples.

        Raises:
            CegalHubError: if an unexpected error is reported by Hub

        Returns:
            Investigation: An object representing the Iris investigation
        """
        return _create_iris_investigation(self._hub_context)

    def load_investigation(self, name: str = None, investigation_id: str = None) -> Investigation:
        """Loads the investigation via Hub

        Note: Either the name or the investigation_id must be defined.

        Args:
            name (str, optional): The name of the investigation to be loaded. Defaults to None.
            investigation_id (str, optional): The id of the investigation to be loaded. Defaults to None.

        Raises:
            CegalHubError: if an unexpected error is reported by Hub
            ValueError: if the supplied parameters are both missing or if it is invalid

        Returns:
            Investigation: An object representing the investigation
        """
        if name is None and investigation_id is None:
            raise ValueError("A name or an investigation_id must be supplied")

        if name is not None:
            investigaton_info = next((inv for inv in self.available_investigations() if inv[1] == name), None)
            if investigaton_info is None:
                raise ValueError("name cannot be found (use available_investigations())")
            investigation_id = investigaton_info.id

        if investigation_id is None:
            raise ValueError("investigation_id must be correctly defined")

        return Investigation(self._hub_context, investigation_id=investigation_id)

    def investigation_from_file(self, path: str) -> Investigation:
        """Creates an investigation from the specified file

        Args:
            path (str): The path to the invpy file

        Raises:
            CegalHubError: if an unexpected error is reported by Hub

        Returns:
            Investigation: An object representing the investigation
        """
        return Investigation(self._hub_context, path=path)

    def investigation_from_dataframe(self,
                                     dataframe: pd.DataFrame,
                                     continuous_column_names: Sequence[str] = None,
                                     continuous_column_info: Dict[str, ContinuousDimensionInfoTuple] = None,
                                     discrete_column_names: Sequence[str] = None,
                                     dataset_column_name: str = None,
                                     sample_index_column_names: Sequence[str] = None) -> Investigation:
        """Creates an investigation from the specified dataframe

        If none of the optional parameters, then the "best" guess of how to represent the dataframe as an investigaton will be used.

        Args:
            dataframe (pd.DataFrame): The input dataframe
            continuous_column_names (Sequence[str], optional): a list of the dataframe column names to include in the investigation as continuous dimensions. Defaults to None.
            continuous_column_info (Dict[str, ContinuousDimensionInfoTuple], optional): a dictionary containing the ContinuousDimensionInfoTuple for each continuous dimension in the investigation. Defaults to None.
            discrete_column_names (Sequence[str], optional): a list of the dataframe column names to include in the investigation as descrete dimensions. Defaults to None.
            dataset_column_name (str, optional): a dataframe column name which should be used to identify different datasets. Defaults to None.
            sample_index_column_names (Sequence[str], optional): a list of the dataframe column names that identify sample index columns. The sample indices will be evaluated in the order of this list. Defaults to None.

        Raises:
            CegalHubError: if an unexpected error is reported by Hub

        Returns:
            Investigation: An object representing the investigation
        """
        return _from_dataframe(self._hub_context,
                               dataframe,
                               continuous_column_names,
                               continuous_column_info,
                               discrete_column_names,
                               dataset_column_name,
                               sample_index_column_names)

    def remove_investigation(self, name: str = None, investigation_id: str = None):
        """This removes an investigation from the Investigtor server

        Removing the investigation will mean its data it can no longer be accessed and it will not be possible to create plots based on the investigation.

        Note: Either the name or the investigation_id must be defined.
        Note: Removal of an investigation is immediate and cannot be reversed.

        Args:
            name (str, optional): The name of the investigation to be removed. Defaults to None.
            investigation_id (str, optional): The id of the investigation to be removed. Defaults to None.

        Raises:
            CegalHubError: if an unexpected error is reported by Hub
            ValueError: if the supplied parameters are both missing or if it is invalid
        """
        if name is None and investigation_id is None:
            raise ValueError("A name or an investigation_id must be supplied")

        if name is not None:
            investigaton_info = next((inv for inv in self.available_investigations() if inv.name == name), None)
            if investigaton_info is None:
                raise ValueError("name cannot be found (use available_investigations())")
            investigation_id = investigaton_info.id

        if investigation_id is None:
            raise ValueError("investigation_id must be correctly defined")

        _remove_investigation(self._hub_context, investigation_id)
