# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2022 Róbert Čerňanský



"""Utilities for component tests and tests for application starter.

Tests are using standard :mod:`unittest` module; they can be ran by the means provided by it or by using the
:mod:`run_tests` module."""



from .component_test_utils import *
from .run_tests import *
from .test_starter import *



__all__ = component_test_utils.__all__ + run_tests.__all__ + test_starter.__all__
