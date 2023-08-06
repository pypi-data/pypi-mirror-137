# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the PetrelInnestigation class
"""

from typing import Sequence

from google.protobuf.any_pb2 import Any

# pylint: disable=relative-beyond-top-level

from .exceptions import CegalHubError
from .hub_context import InvPyHubContext
from .protos import petrel_pb2
from .protos import investigator_api_pb2


class PetrelInvestigation:
    """This class represent a new Petrel investigation

    DO NOT USE
    """
    def __init__(self,
                 hub_context: InvPyHubContext,
                 name: str,
                 num_continuous_dimensions: int,
                 num_discrete_dimensions: int = 0,
                 add_spatial_x: bool = False,
                 add_spatial_y: bool = False,
                 add_spatial_depth: bool = False,
                 add_spatial_time: bool = False):

        self._hub_context = hub_context
        self._name = name
        self._num_continuous_dimensions = num_continuous_dimensions
        self._num_discrete_dimensions = num_discrete_dimensions
        self._add_spatial_x = add_spatial_x
        self._add_spatial_y = add_spatial_y
        self._add_spatial_depth = add_spatial_depth
        self._add_spatial_depth = add_spatial_time
        self._datasets = []

    def add_dataset(self,
                    domain_object_ids: Sequence[str],
                    continuous_object_ids: Sequence[str],
                    discrete_object_ids: Sequence[str]):
        dataset = petrel_pb2.PetrelDataset()
        for domain_object_id in domain_object_ids:
            dataset.data_object_ids.append(domain_object_id)
        for continuous_object_id in continuous_object_ids:
            dataset.continuous_data_ids.append(continuous_object_id)
        for discrete_object_id in discrete_object_ids:
            dataset.discrete_data_ids.append(discrete_object_id)

        self._datasets.append(dataset)

    def create(self):
        msg = petrel_pb2.CreatePetrelInvestigation()
        msg.name = self._name
        msg.num_continuous_dimensions = self._num_continuous_dimensions
        msg.num_discrete_dimensions = self._num_discrete_dimensions
        msg.include_spatial_x = self._add_spatial_x
        msg.include_spatial_y = self._add_spatial_y
        msg.include_spatial_depth = self._add_spatial_depth
        msg.include_spatial_time = self._add_spatial_depth
        for dataset in self._datasets:
            msg.datasets.append(dataset)

        payload = Any()
        payload.Pack(msg)

        result = self._hub_context.do_unary_request("investigator.create",
                                                    payload,
                                                    wellknown_connector_identifier="cegal.hub.petrel")
        if result[0]:
            response = investigator_api_pb2.InvestigationSummary()
            result[1].Unpack(response)
            return response.id
        else:
            raise CegalHubError(result[1])
