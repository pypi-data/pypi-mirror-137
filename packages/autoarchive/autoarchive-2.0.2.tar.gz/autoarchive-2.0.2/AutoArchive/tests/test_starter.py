# test_starter.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2022 Róbert Čerňanský



""":class:`TestStarter`."""



__all__ = ["TestStarter"]



# {{{ INCLUDES

import unittest

from ..starter import Starter
from .component_test_utils import ComponentTestUtils
from AutoArchive._infrastructure.configuration.tests import ConfigurationTestUtils

# }}} INCLUDES



# {{{ CLASSES
from .._application.archiving.archive_spec.tests import ArchiveSpecTestUtils



class TestStarter(unittest.TestCase):
    """Test of basic use cases of public API of :meth:`.Starter` class."""

    @classmethod
    def setUpClass(cls):
        ComponentTestUtils.setUpClassComponent()


    @classmethod
    def tearDownClass(cls):
        ComponentTestUtils.tearDownClassComponent()



    def setUp(self):
        ConfigurationTestUtils.makeUserConfigDirectory()
        ConfigurationTestUtils.makeArchiveSpecsDirectory()



    def tearDown(self):
        ConfigurationTestUtils.removeArchiveSpecsDirectory()
        ConfigurationTestUtils.removeUserConfigDirectory()
        ComponentTestUtils.checkWorkDirEmptiness()



    def test_startExitCode0(self):
        "Tests :meth:`.Starter.start()` method for the exit code in case of an action success."

        ArchiveSpecTestUtils.makeArchiveSpecFile()

        exitCode = Starter.start(args =
        ["test_app_name",
         str.format("--user-config-dir={}", ComponentTestUtils.getComponentTestContext().userConfigDir),
         str.format("--archive-specs-dir={}", ComponentTestUtils.getComponentTestContext().archiveSpecsDir),
         "--list"])

        self.assertEqual(0, exitCode)



    def test_startFalseAction(self):
        "Tests :meth:`.Starter.start()` method for the exit code in case of an action failure."

        exitCode = Starter.start(args = [
            "test_app_name",
            str.format("--user-config-dir={}", ComponentTestUtils.getComponentTestContext().userConfigDir),
            "non_existing_archive"])

        self.assertEqual(1, exitCode)

# }}} CLASSES
