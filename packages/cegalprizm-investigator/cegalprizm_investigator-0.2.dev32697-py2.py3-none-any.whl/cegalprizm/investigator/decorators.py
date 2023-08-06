# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.


"""This file contains the decorators that must be used to document the data format the functions expect when called from Investigator
"""

# pylint: disable=invalid-name

from typing import Callable

# This must match the same chunk of code in Crossplots.Scripting.ScriptingUtils


# def to_nparray(net_array):
#     import numpy as np
#     # assume array is regular
#     rows = net_array.GetLength(0)
#     cols = net_array[0].GetLength(0)
#     nparray = np.empty((rows, cols), np.float64)
#     for row_idx in range(0, rows):
#         for col_idx in range(0, cols):
#             nparray[row_idx, col_idx] = net_array[row_idx][col_idx]
#     return nparray


def InvestigatorPyFunction1D(func: Callable):
    """This decorator should be used to indicate that the function expects input data in the form of a 1D array per sample

    The decorated function will be treated as if typed as follows:

        function calculate(input: double[]) -> double

    Investigator will ensure that only a single sample is passed to the function.
    The function is expected to return a single output value.

    Args:
        func (Callable): The function being decoarated
    """
    def InvestigatorPyFunction1D_decorator(f):
        def wrapper(inputs):
            return tuple([f(i) for i in inputs])
        return wrapper
    return InvestigatorPyFunction1D_decorator(func)


def InvestigatorPyFunction2D(func: Callable):
    """This decorator should be used to indicate that the function expects input data in the form of a 2D array.

    The decorated function will be treated as if typed as follows:

        function calculate(input: double[][]) -> double[]

    Investigator will ensure that an array of samples is passed to the function. Each sample in the array will contain an array of input value.
    The function is expected to return an array of output values where each value is the output from processing a single sample.

    Args:
        func (Callable): The function being decoarated
    """
    def InvestigatorPyFunction2D_decorator(f):
        def wrapper2D(inputs):
            return tuple(f(inputs))
        return wrapper2D
    return InvestigatorPyFunction2D_decorator(func)
