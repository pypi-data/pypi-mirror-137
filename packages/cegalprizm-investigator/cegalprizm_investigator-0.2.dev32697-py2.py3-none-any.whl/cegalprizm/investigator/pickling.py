# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the methods to be used to save predictors and classifiers to files that can be transferred back to Blueback Investigator
"""

from typing import Callable, Sequence

import json
import base64
import cloudpickle


def save_classifier(filename: str, func: Callable, inputs: Sequence[tuple], output: tuple):
    """Saves a classifier function to 'filename'

    Args:
        filename (str):
            the name of the file to be created
        func (function):
            the function that should be invoked to run the classifier
        inputs (list):
            a list of tuples each containing a continuous dimension name and a unit string
            (see Investigation.available_units property)
        output (tuple):
            a tuple of discrete dimension name, list of discrete tags
            (see Investigation.discrete_dimension_tags property)

    Output:
        json: A JSON file containing all the required information to define the classifier and the pickled classifier function
    """

    if not isinstance(filename, str):
        raise ValueError("filename invalid: must be a str")
    if len(filename) == 0:
        raise ValueError("filename invalid: must contain text")

    if not isinstance(inputs, list):
        raise ValueError("inputs invalid: must be a list")
    if len(inputs) == 0:
        raise ValueError("inputs invalid: must contain at least 1 element")
    if not all(isinstance(item, tuple) for item in inputs):
        raise ValueError("inputs invalid: must be a list of tuples")

    if not isinstance(output, tuple):
        raise ValueError("output invalid: must be a tuple")

    data = {
        'inputs': [[item[0], item[1]] for item in inputs],
        'output': {output[0]: output[1]},
        'function': base64.b64encode(cloudpickle.dumps(func)).decode("utf-8")
    }

    # with open(filename + ".pickle", "wb") as f:
    #    cloudpickle.dump(func, f)

    with open(filename + ".json", "w") as f:
        json.dump(data, f, indent=4)


def load_classifier(filename: str):
    """Loads a function from 'filename'

    Args:
        filename (str): The filename

    Returns:
        [type]: [description]
    """
    with open(filename + ".json", "r") as f:
        data = json.load(f)

    inputs = data["inputs"]
    output = data["output"]
    function = cloudpickle.loads(base64.b64decode(data["function"]))

    output_key = list(output.keys())[0]
    return (inputs, (output_key, output[output_key]), function)


def save_predictor(filename: str, func: Callable, inputs: Sequence[tuple], output: tuple):
    """Saves a predictor function to 'filename'

    Args:
        filename (str):
            the name of the file to be created
        func (function):
            the name of the function that should be invoked to run the predictor
        inputs (list):
            a list of tuples each containing a continuous dimension name and a unit string
            (see Investigation.available_units property)
        output (tuple):
            a tuple of continuous dimension name, a unit string
            (see Investigation.available_units property)

    Outputs:
        json: A JSON file containing all the required information to define the predictor and the pickled predictor function
    """

    if not isinstance(filename, str):
        raise ValueError("filename invalid: must be a str")
    if len(filename) == 0:
        raise ValueError("filename invalid: must contain text")

    if not isinstance(inputs, list):
        raise ValueError("inputs invalid: must be a list")
    if len(inputs) == 0:
        raise ValueError("inputs invalid: must contain at least 1 element")
    if not all(isinstance(item, tuple) for item in inputs):
        raise ValueError("inputs invalid: must be a list of tuples")

    if not isinstance(output, tuple):
        raise ValueError("output invalid: must be a tuple")

    data = {
        'inputs': [[item[0], item[1]] for item in inputs],
        'output': {output[0]: output[1]},
        'function': base64.b64encode(cloudpickle.dumps(func)).decode("utf-8")
    }

    # with open(filename + ".pickle", "wb") as f:
    #    cloudpickle.dump(func, f)

    with open(filename + ".json", "w") as f:
        json.dump(data, f, indent=4)


def load_predictor(filename: str):
    """Loads a function from 'filename'

    Returns:
        cloudpickle: file
    """

    with open(filename + ".json", "r") as f:
        data = json.load(f)

    inputs = data["inputs"]
    output = data["output"]
    function = cloudpickle.loads(base64.b64decode(data["function"]))

    output_key = list(output.keys())[0]
    return (inputs, (output_key, output[output_key]), function)
