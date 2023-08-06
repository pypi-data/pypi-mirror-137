# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""The cegalprizm.investigator module provides the API to allow Blueback Investigations to be accessed from Python.
"""

__version__ = '0.2.0'
__git_hash__ = '3c6a64ec'

import logging
logger = logging.getLogger(__name__)

# pylint: disable=wrong-import-position

from .connection import InvestigatorConnection
from .config import Config
from .decorators import InvestigatorPyFunction1D
from .decorators import InvestigatorPyFunction2D
from .named_tuples import *
from .pickling import *
from .petrel import PetrelInvestigation
from .plotting import *
from .statistics import *

from .inv.investigation import Investigation

from .views import *
