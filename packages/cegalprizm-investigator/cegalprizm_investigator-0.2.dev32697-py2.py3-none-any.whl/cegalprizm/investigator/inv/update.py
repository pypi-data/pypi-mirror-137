# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the method to update the server investigation based on the local investigation
"""

from typing import Type

from google.protobuf.any_pb2 import Any

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..exceptions import CegalHubError
from ..protos import investigator_api_pb2

from .investigation  import Investigation

def _update_investigation(investigation: Type[Investigation]):
    msg = investigator_api_pb2.SetContinuousDimensionInfo()
    msg.investigation_id.id = investigation._info.id
    for dimension_info in investigation._continuous_dimensions.values:
        msg.values.append(dimension_info)

    payload = Any()
    payload.Pack(msg)

    result = investigation._hub_context.do_unary_request("investigator.SetContinuousDimensions", payload)
    if result[0]:
        response = investigator_api_pb2.ContinuousDimensionInfoCollection()
        result[1].Unpack(response)
        investigation._continuous_dimensions = response
    else:
        raise CegalHubError(result[1])

    msg = investigator_api_pb2.SetDiscreteDimensionInfo()
    msg.investigation_id.id = investigation._info.id
    for dimension_info in investigation._discrete_dimensions.values:
        msg.values.append(dimension_info)

    payload = Any()
    payload.Pack(msg)

    result = investigation._hub_context.do_unary_request("investigator.SetDiscreteDimensions", payload)
    if result[0]:
        response = investigator_api_pb2.DiscreteDimensionInfoCollection()
        result[1].Unpack(response)
        investigation._discrete_dimensions = response
    else:
        raise CegalHubError(result[1])

    msg = investigator_api_pb2.SetDatasetInfo()
    msg.investigation_id.id = investigation._info.id
    for dataset_tuple in investigation._get_datasets(investigation._datasets):
        msg.values.append(dataset_tuple[0])

    payload = Any()
    payload.Pack(msg)

    result = investigation._hub_context.do_unary_request("investigator.SetDatasets", payload)
    if result[0]:
        response = investigator_api_pb2.DatasetInfoCollection()
        result[1].Unpack(response)
        investigation._datasets = response
    else:
        raise CegalHubError(result[1])
