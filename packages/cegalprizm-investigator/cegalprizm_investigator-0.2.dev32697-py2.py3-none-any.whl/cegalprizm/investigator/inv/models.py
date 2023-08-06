# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the methods for creating prediction and classification equations in an investigation
"""

from typing import Callable, Sequence, Type

import base64
import cloudpickle

from google.protobuf.any_pb2 import Any

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from .. import logger
from ..exceptions import CegalHubError
from ..named_tuples import ContinuousPropertyTuple, DiscretePropertyTuple
from ..protos import investigator_api_pb2
from ..utils import _CHUNK_SIZE, _pack_payloads

from .investigation import Investigation

def __get_chunks(investigation_id: str, model_id: str, model_type: investigator_api_pb2.ModelEnum, func: Callable):

    func_string = base64.b64encode(cloudpickle.dumps(func)).decode("utf-8")

    pos = 0
    length = len(func_string)
    while pos < length:
        if pos + _CHUNK_SIZE < length:
            end = pos + _CHUNK_SIZE
        else:
            end = length
        msg = investigator_api_pb2.UploadModelChunk()
        msg.investigation_id.id = investigation_id
        msg.model_id = model_id
        msg.model_type = model_type
        msg.chunk.buffer = func_string[pos:end].encode("utf-8")
        yield msg
        pos += _CHUNK_SIZE


def _save_classifier(investigation: Type[Investigation], name: str, func: Callable, inputs: Sequence[ContinuousPropertyTuple], output: DiscretePropertyTuple):

    if not isinstance(inputs, list):
        raise ValueError("inputs invalid: must be a list")
    if len(inputs) == 0:
        raise ValueError("inputs invalid: must contain at least 1 element")
    if not all(isinstance(item, tuple) for item in inputs):
        raise ValueError("inputs invalid: must be a list of tuples")
    if not isinstance(output, tuple):
        raise ValueError("output invalid: must be a tuple")

    msg = investigator_api_pb2.CreateModelRequest()
    msg.investigation_id.id = investigation._info.id
    msg.name = name

    for item in inputs:
        model_input = investigator_api_pb2.ModelInput()
        dimension_info = next((x for x in investigation._continuous_dimensions.values if x.name == item.name), None)
        if dimension_info is None:
            raise ValueError(f"inputs list item[0] must be one of {str(investigation.dataset_names)}")
        model_input.name = item.name
        model_input.id = dimension_info.id
        model_input.unit = item.unit_symbol
        msg.inputs.append(model_input)

    msg.classifier_output.name = output.name
    for index, tag_name in enumerate(output.tags):
        tag = investigator_api_pb2.ClassifierTag()
        tag.name = tag_name
        tag.value = index
        msg.classifier_output.tags.append(tag)

    payload = Any()
    payload.Pack(msg)

    result = investigation._hub_context.do_unary_request("investigator.CreateModel", payload)
    if result[0]:
        response = investigator_api_pb2.CreateModelResponse()
        result[1].Unpack(response)
        model_id = response.model_id
        model_type = response.model_type
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_client_streaming("investigator.UploadModel", _pack_payloads(__get_chunks(investigation._info.id, model_id, model_type, func)))
    if result[0]:
        logger.info(f"Created classifier {name} in investigation")
        return
    else:
        raise CegalHubError(result[1])


def _save_predictor(investigation: Type[Investigation], name: str, func: Callable, inputs: Sequence[ContinuousPropertyTuple], output: ContinuousPropertyTuple):
    if not isinstance(inputs, list):
        raise ValueError("inputs invalid: must be a list")
    if len(inputs) == 0:
        raise ValueError("inputs invalid: must contain at least 1 element")
    if not all(isinstance(item, tuple) for item in inputs):
        raise ValueError("inputs invalid: must be a list of tuples")
    if not isinstance(output, tuple):
        raise ValueError("output invalid: must be a tuple")

    msg = investigator_api_pb2.CreateModelRequest()
    msg.investigation_id.id = investigation._info.id
    msg.name = name

    for item in inputs:
        model_input = investigator_api_pb2.ModelInput()
        dimension_info = next((x for x in investigation._continuous_dimensions.values if x.name == item.name), None)
        if dimension_info is None:
            raise ValueError(f"inputs list item.name must be one of {str(investigation.dataset_names)}")
        model_input.name = item.name
        model_input.id = dimension_info.id
        model_input.unit = item.unit_symbol
        msg.inputs.append(model_input)

    msg.predictor_output.name = output.name
    msg.predictor_output.unit = output.unit_symbol

    payload = Any()
    payload.Pack(msg)

    result = investigation._hub_context.do_unary_request("investigator.CreateModel", payload)
    if result[0]:
        response = investigator_api_pb2.CreateModelResponse()
        result[1].Unpack(response)
        model_id = response.model_id
        model_type = response.model_type
    else:
        raise CegalHubError(result[1])

    result = investigation._hub_context.do_client_streaming("investigator.UploadModel", _pack_payloads(__get_chunks(investigation._info.id, model_id, model_type, func)))
    if result[0]:
        logger.info(f"Created predictor {name} in investigation")
        return
    else:
        raise CegalHubError(result[1])
