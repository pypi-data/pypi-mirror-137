# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the method to refresh the local cached investigation object from the server
"""

from typing import Type

from google.protobuf.any_pb2 import Any

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..exceptions import CegalHubError
from ..protos import investigation_pb2
from ..protos import investigator_api_pb2

from .investigation import Investigation

def _refresh(investigation: Type[Investigation]):
    msg = investigator_api_pb2.InvestigationId(id=investigation._info.id)
    payload = Any()
    payload.Pack(msg)

    result = investigation._hub_context.do_unary_request("investigator.GetContinuousDimensions", payload)
    if result[0]:
        response = investigator_api_pb2.ContinuousDimensionInfoCollection()
        result[1].Unpack(response)
        investigation._continuous_dimensions = response
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_unary_request("investigator.GetDiscreteDimensions", payload)
    if result[0]:
        response = investigator_api_pb2.DiscreteDimensionInfoCollection()
        result[1].Unpack(response)
        investigation._discrete_dimensions = response
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_unary_request("investigator.GetClassifications", payload)
    if result[0]:
        response = investigation_pb2.Classifications()
        result[1].Unpack(response)
        investigation._classification_groups = response
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_unary_request("investigator.GetRestrictions", payload)
    if result[0]:
        response = investigation_pb2.Restrictions()
        result[1].Unpack(response)
        investigation._restrictions = response
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_unary_request("investigator.GetDatasets", payload)
    if result[0]:
        response = investigator_api_pb2.DatasetInfoCollection()
        result[1].Unpack(response)
        investigation._datasets = response
    else:
        raise CegalHubError(result[1])

    investigation._dataset_additional_discrete = list(investigation._get_additional_discrete())
