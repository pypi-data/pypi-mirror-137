# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the method to create a dataframe from an investiation
"""

from typing import Sequence, Type, Union

import pandas as pd
from google.protobuf.any_pb2 import Any

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..exceptions import CegalHubError
from ..protos import investigation_pb2
from ..protos import investigator_api_pb2

from .investigation  import Investigation


def _to_dataframe(investigation: Type[Investigation],
                  dataset_name: str = None,
                  continuous_columns: Union[str, Sequence[str]] = "all",
                  continuous_units: str = "display",
                  discrete_columns: Union[str, Sequence[str]] = "all",
                  discrete_data_as: str = "string",
                  include_filters: Union[str, Sequence[str]] = "all"):
    if continuous_columns == "all":
        continuous_column_names = [dimension.name for dimension in investigation._continuous_dimensions.values]
    elif continuous_columns is None:
        continuous_column_names = []
    elif isinstance(continuous_columns, list):
        continuous_column_names = []
        for col in continuous_columns:
            continuous_valid = False
            for dimension in investigation._continuous_dimensions.values:
                if col == dimension.name:
                    continuous_column_names.append(dimension.name)
                    continuous_valid = True
                    break
            if not continuous_valid:
                raise ValueError(f"continuous_columns invalid: {col} is not a valid continuous column name")
    else:
        raise ValueError("continuous_columns invalid: must be 'all' or list or None")

    selected_continuous_dimensions = []

    if continuous_units == "invariant":
        for col in continuous_column_names:
            for dimension in investigation._continuous_dimensions.values:
                if col == dimension.name:
                    selected_continuous_dimensions.append(__get_continuous_query_info(dimension, "invariant"))
                    break
    elif continuous_units == "display":
        for col in continuous_column_names:
            for dimension in investigation._continuous_dimensions.values:
                if col == dimension.name:
                    selected_continuous_dimensions.append(__get_continuous_query_info(dimension, "display"))
                    break
    elif isinstance(continuous_units, dict):
        all_units = investigation.available_units
        custom_units_valid = True
        for key in continuous_column_names:
            if key not in continuous_units.keys():
                custom_units_valid = False
                raise KeyError(f"continuous_units invalid: units for {key} are missing")
        for key in continuous_units.keys():
            if key in continuous_column_names:
                if continuous_units[key] not in all_units[key]:
                    custom_units_valid = False
                    raise ValueError(f"continuous_units invalid: specified units for {key} are not supported")
            else:
                custom_units_valid = False
                raise ValueError(f"continuous_units invalid: {key} is not a valid continuous column name")
        if custom_units_valid:
            for key in continuous_units.keys():
                for dimension in investigation._continuous_dimensions.values:
                    if key == dimension.name:
                        selected_continuous_dimensions.append(__get_continuous_query_info(dimension, continuous_units[key]))
                        break
    else:
        raise ValueError("continuous_units invalid: supported values are 'display' or 'invariant' or dict")

    # print(selected_continuous_dimensions)

    if discrete_data_as != "string" and discrete_data_as != "value":
        raise ValueError("discrete_data_as invalid: must be 'string' or 'value'")

    if discrete_columns == "all":
        include_dataset_column = True
        selected_discrete_column_names = []
        selected_discrete_dimensions = []
        selected_classification_names = []
        selected_classification_ids = []
        selected_dataset_discrete_names = []
        selected_additional_discrete = []
        for dimension in investigation._discrete_dimensions.values:
            selected_discrete_column_names.append(dimension.name)
            selected_discrete_dimensions.append(__get_discrete_query_info(dimension))
        for classification in investigation._classification_groups.values:
            selected_classification_names.append(classification.name)
            selected_classification_ids.append(__get_classification_query_info(classification))
        for additional_discrete in investigation._dataset_additional_discrete:
            selected_dataset_discrete_names.append(additional_discrete[1].name)
            selected_additional_discrete.append(__get_additional_discrete_query_info(additional_discrete))
    elif discrete_columns is None:
        include_dataset_column = False
        selected_discrete_column_names = []
        selected_discrete_dimensions = []
        selected_classification_names = []
        selected_classification_ids = []
        selected_dataset_discrete_names = []
        selected_additional_discrete = []
    elif isinstance(discrete_columns, list):
        include_dataset_column = False
        selected_discrete_column_names = []
        selected_discrete_dimensions = []
        selected_classification_names = []
        selected_classification_ids = []
        selected_dataset_discrete_names = []
        selected_additional_discrete = []
        for col in discrete_columns:
            discrete_valid = False
            if col == investigation.DATASET_DIMENSION_NAME:
                include_dataset_column = True
                discrete_valid = True
            if not discrete_valid:
                for dimension in investigation._discrete_dimensions.values:
                    if col == dimension.name:
                        selected_discrete_column_names.append(dimension.name)
                        selected_discrete_dimensions.append(__get_discrete_query_info(dimension))
                        discrete_valid = True
                        break
            if not discrete_valid:
                for classification_group in investigation._classification_groups.values:
                    if col == classification_group.name:
                        selected_classification_names.append(classification_group.name)
                        selected_classification_ids.append(__get_classification_query_info(classification_group))
                        discrete_valid = True
                        break
            if not discrete_valid:
                for additional_discrete in investigation._dataset_additional_discrete:
                    if col == additional_discrete[1].name:
                        selected_dataset_discrete_names.append(additional_discrete[1].name)
                        selected_additional_discrete.append(__get_additional_discrete_query_info(additional_discrete))
                        discrete_valid = True
                        break
            if not discrete_valid:
                raise ValueError(f"discrete_columns invalid: {col} is not a valid discrete column name")
    else:
        raise ValueError("discrete_columns invalid: must be 'all' or list or None")

    # print(selected_discrete_column_names)
    # print(selected_discrete_dimensions)
    # print(selected_classification_names)
    # print(selected_classification_ids)
    # print(selected_dataset_discrete_names)
    # print(selected_additional_discrete)

    discrete_tuples = investigation._discrete_tuples()
    discrete_lookups = []
    for name in selected_discrete_column_names:
        discrete_lookups.append(__get_tag_lookup(discrete_tuples, name, discrete_data_as))
    for name in selected_classification_names:
        discrete_lookups.append(__get_tag_lookup(discrete_tuples, name, discrete_data_as))
    for name in selected_dataset_discrete_names:
        discrete_lookups.append(__get_tag_lookup(discrete_tuples, name, discrete_data_as))

    dataset_column_name = []
    dataset_lookup = []
    if include_dataset_column:
        dataset_column_name.append(investigation.DATASET_DIMENSION_NAME)
        dataset_lookup.append(__get_tag_lookup(discrete_tuples, investigation.DATASET_DIMENSION_NAME, discrete_data_as))

    discrete_column_names = dataset_column_name + selected_discrete_column_names + selected_classification_names + selected_dataset_discrete_names

    # print(discrete_column_names)
    # print(dataset_lookup)
    # print(discrete_lookups)

    if include_filters == "all":
        selected_filter_ids = []
        filter_names = []
        for value in investigation._restrictions.values:
            if investigation_pb2.RestrictionTypeEnum.Name(value.type) == 'Filter':
                selected_filter_ids.append(value.id)
                filter_names.append(value.name)
    elif isinstance(include_filters, list):
        selected_filter_ids = []
        filter_names = []
        for col in include_filters:
            filter_valid = False
            for value in investigation._restrictions.values:
                if col == value.name and investigation_pb2.RestrictionTypeEnum.Name(value.type) == 'Filter':
                    selected_filter_ids.append(value.id)
                    filter_names.append(value.name)
                    filter_valid = True
                    break
            if not filter_valid:
                raise ValueError(f"include_filters invalid: {col} is not a valid filter name")
    elif include_filters is None:
        selected_filter_ids = []
        filter_names = []
    else:
        raise ValueError("include_filters invalid: must be 'all' or list or None")

    # print(filter_names)

    if dataset_name is None:
        selected_dataset_ids = [t[0].id for t in investigation._get_datasets(investigation._datasets)]
    else:
        dataset_found = False
        for dataset_tuple in investigation._get_datasets(investigation._datasets):
            if dataset_tuple[0].name == dataset_name:
                selected_dataset_ids = [dataset_tuple[0].id]
                dataset_found = True
                break
        if not dataset_found:
            raise ValueError("dataset_name invalid: must be a valid dataset name or None")

    # print(selected_dataset_ids)

    frames = []

    msg = investigator_api_pb2.DataframeQuery()
    msg.investigation_id.id = investigation.id
    msg.selected_datasets.ids.extend(selected_dataset_ids)
    msg.selected_continuous_dimensions.dimensions.extend(selected_continuous_dimensions)
    msg.selected_discrete_dimensions.dimensions.extend(selected_discrete_dimensions)
    msg.selected_filters.ids.extend(selected_filter_ids)
    msg.selected_classfications.ids.extend(selected_classification_ids)
    msg.selected_additional_discrete.values.extend(selected_additional_discrete)

    payload = Any()
    payload.Pack(msg)

    for result in investigation._hub_context.do_server_streaming("investigator.GetData", payload):
        if result[0]:
            response = investigator_api_pb2.DataframeRowsCollection()
            if result[1].Is(response.DESCRIPTOR):
                result[1].Unpack(response)

                for index, dataset_tuple in enumerate(investigation._get_datasets(investigation._datasets)):
                    if dataset_tuple[0].id == response.dataset_id:
                        if discrete_data_as == "string":
                            dataset_value = dataset_tuple[1]
                        else:
                            dataset_value = index
                        break

                # for row in response.rows:
                #     print(list(row.continuous_values) +
                #           [dataset_value] +
                #           list(map(lambda v, l: l[v], row.discrete_values, discrete_lookups)) +
                #           list(row.filter_values))

                if include_dataset_column:
                    temp_dataframe = pd.DataFrame.from_records(tuple(list(row.continuous_values) +
                                                                     [dataset_value] +
                                                                     list(map(lambda v, l: l[v], row.discrete_values, discrete_lookups)) +
                                                                     list(row.filter_values)) for row in response.rows)
                else:
                    temp_dataframe = pd.DataFrame.from_records(tuple(list(row.continuous_values) +
                                                                     list(map(lambda v, l: l[v], row.discrete_values, discrete_lookups)) +
                                                                     list(row.filter_values)) for row in response.rows)
                frames.append(temp_dataframe)
        else:
            raise CegalHubError(result[1])

    dataframe = pd.concat(frames, ignore_index=True)
    dataframe.columns = continuous_column_names + discrete_column_names + filter_names

    return dataframe


def __get_continuous_query_info(dimension, unit: str = 'display'):
    info = investigator_api_pb2.QueryContinuousInfo()
    info.id = dimension.id
    if unit == 'display':
        info.unit = dimension.display_units
    elif unit == 'invariant':
        info.unit = dimension.invariant_units
    else:
        info.unit = unit
    return info


def __get_discrete_query_info(dimension):
    info = investigator_api_pb2.QueryDiscreteInfo()
    info.id = dimension.id
    return info


def __get_classification_query_info(classification_group):
    return classification_group.id


def __get_additional_discrete_query_info(additional_discrete):
    info = investigator_api_pb2.AdditionalDiscrete()
    info.dataset_id = additional_discrete[0]
    info.discrete_id = additional_discrete[1].id
    return info


def __get_tag_lookup(discrete_tuples, name, discrete_data_as):
    options = discrete_tuples[name]
    if discrete_data_as == "string":
        return {t[0]: t[2] for t in options}
    else:
        return {t[0]: options.index(t) for t in options}
