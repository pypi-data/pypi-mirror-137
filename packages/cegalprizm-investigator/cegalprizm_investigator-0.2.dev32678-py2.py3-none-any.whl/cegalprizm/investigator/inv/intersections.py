# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the methods for creating intersections between datasets in an investigation
"""

from typing import Type, Sequence

from google.protobuf.any_pb2 import Any

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..exceptions import CegalHubError
from ..protos import investigator_api_pb2

from .investigation import Investigation

def _create_borehole_intersections(investigation: Type[Investigation], grid_names: Sequence[str]):
    dataset_tuples = list(investigation._get_datasets(investigation._datasets))

    msg = investigator_api_pb2.CreateIntersections()
    msg.investigation_id.id = investigation._info.id
    msg.create_borehole_intersections = True
    msg.create_maps = False

    for name in grid_names:
        found = False
        for dataset_tuple in dataset_tuples:
            if dataset_tuple[0].name == name:
                msg.selected_grids.append(dataset_tuple[0].id)
                found = True
        if not found:
            raise ValueError(f"{name} is not valid")

    payload = Any()
    payload.Pack(msg)

    result = investigation._hub_context.do_unary_request("investigator.CreateIntersections", payload)
    if result[0]:
        investigation.refresh()
        return
    else:
        raise CegalHubError(result[1])

def _create_map_intersections(investigation: Type[Investigation], grid_names: Sequence[str]):
    dataset_tuples = list(investigation._get_datasets(investigation._datasets))

    msg = investigator_api_pb2.CreateIntersections()
    msg.investigation_id.id = investigation._info.id
    msg.create_borehole_intersections = False
    msg.create_maps = True

    for name in grid_names:
        found = False
        for dataset_tuple in dataset_tuples:
            if dataset_tuple[0].name == name:
                msg.selected_grids.append(dataset_tuple[0].id)
                found = True
        if not found:
            raise ValueError(f"{name} is not valid")

    payload = Any()
    payload.Pack(msg)

    result = investigation._hub_context.do_unary_request("investigator.CreateIntersections", payload)
    if result[0]:
        investigation.refresh()
        return
    else:
        raise CegalHubError(result[1])
