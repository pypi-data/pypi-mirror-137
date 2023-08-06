# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the custom exceptions that can be raised by Investigator
"""


class CegalHubError(Exception):
    """This exception is raised when an unexpected error is reported by Hub

    Args:
        Exception: The exception
    """

class InvestigatorViewError(Exception):
    """This exception is raised when trying to use a view that is not supported in by the investigation

    Args:
        Exception: The exception
    """
