# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains private methods which should only be used internally
"""

from typing import List

from google.protobuf.any_pb2 import Any

# pylint: disable=relative-beyond-top-level

from . import logger
from .exceptions import CegalHubError
from .hub_context import InvPyHubContext
from .named_tuples import InvestigationInfoTuple
from .protos import common_pb2
from .protos import investigator_api_pb2


def _get_available_investigations(context: InvPyHubContext) -> List[investigator_api_pb2.InvestigationSummary]:
    msg = common_pb2.EmptyMessage()
    payload = Any()
    payload.Pack(msg)

    available = []
    for result in context.do_server_streaming("investigator.ListInvestigations", payload):
        logger.debug(result)
        if result[0]:
            response = investigator_api_pb2.InvestigationSummary()
            if result[1].Is(response.DESCRIPTOR):
                if result[1].Unpack(response):
                    available.append(response)
        else:
            raise CegalHubError(result[1])
    return available


def _available_investigations(context: InvPyHubContext) -> List[InvestigationInfoTuple]:
    result = []
    for info in _get_available_investigations(context):
        result.append(InvestigationInfoTuple(id=info.id, name=info.name))
    return result

def _remove_investigation(context: InvPyHubContext, investigation_id: str):
    msg = investigator_api_pb2.InvestigationId(id=investigation_id)
    payload = Any()
    payload.Pack(msg)

    result = context.do_unary_request("investigator.DeleteInvestigation", payload)
    if result[0]:
        return
    else:
        raise CegalHubError(result[1])
