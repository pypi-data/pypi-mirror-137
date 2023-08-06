# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains a private method which should only be used internally
"""

from google.protobuf.any_pb2 import Any

# pylint: disable=relative-beyond-top-level
# pylint: disable=logging-fstring-interpolation

from . import logger
from .exceptions import CegalHubError
from .hub_context import InvPyHubContext
from .inv.investigation import Investigation
from .protos import common_pb2
from .protos import investigator_api_pb2


def _create_iris_investigation(context: InvPyHubContext):
    msg = common_pb2.EmptyMessage()
    payload = Any()
    payload.Pack(msg)

    result = context.do_unary_request("investigator.CreateIrisInvestigation", payload)
    if result[0]:
        response = investigator_api_pb2.InvestigationSummary()
        result[1].Unpack(response)
        logger.info(f"Created investigation: {response.id}")
        return Investigation(context, investigation_id=response.id)
    else:
        raise CegalHubError(result[1])
