import os
import shutil
import logging
import unittest
from maya import cmds
from mayaunittest.constants import TEMP_DIRECTORY


class MayaTestCase(unittest.TestCase):
    """
    A maya test case class that contains a few utility functions to manage
    plugin loading and file path generation. It also allows settings at
    class variable level that determine when the file new command is called,
    by default this is between every test. By default logging is disabled but
    can be adjusted by setting the logging level.
    """
    FILE_NEW_DISABLE = 0
    FILE_NEW_ONCE = 1
    FILE_NEW_ALWAYS = 2

    file_new = FILE_NEW_ALWAYS
    logging_level = logging.CRITICAL
    unload_plugin_queue = set()

    @classmethod
    def setUpClass(cls):
        super(MayaTestCase, cls).setUpClass()
        logging.disable(cls.logging_level)

        if cls.file_new is MayaTestCase.FILE_NEW_ONCE:
            cmds.file(newFile=True, force=True)

    @classmethod
    def tearDownClass(cls):
        super(MayaTestCase, cls).tearDownClass()
        logging.disable(logging.NOTSET)

        if cls.file_new in (MayaTestCase.FILE_NEW_ONCE, MayaTestCase.FILE_NEW_ALWAYS):
            cmds.file(newFile=True, force=True)

        cls.delete_temp_directory()
        cls.unload_plugins()

    # ------------------------------------------------------------------------

    @classmethod
    def get_temp_path(cls, *names):
        """
        :param str names:
        :return: Temporary path
        :rtype: str
        :raise RuntimeError: When no names are provided
        """
        if not names:
            raise RuntimeError("Please provide name(s), "
                               "base temp directory is protected.")

        path = os.path.join(TEMP_DIRECTORY, *names)
        directory, _ = os.path.splitext(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        return path

    @classmethod
    def delete_temp_directory(cls):
        if os.path.isdir(TEMP_DIRECTORY):
            shutil.rmtree(TEMP_DIRECTORY, ignore_errors=True)

    # ------------------------------------------------------------------------

    @classmethod
    def load_plugin(cls, plugin):
        """
        Load maya plugin, only if the plugin is not loaded by default it will
        be added to the plugins that will be unloaded at class teardown.

        :param str plugin:
        """
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            cmds.loadPlugin(plugin)
            cls.unload_plugin_queue.add(plugin)

    @classmethod
    def unload_plugins(cls):
        for plugin in cls.unload_plugin_queue:
            cmds.unloadPlugin(plugin)
        cls.unload_plugin_queue.clear()

    # ------------------------------------------------------------------------

    def setUp(self):
        if self.file_new is MayaTestCase.FILE_NEW_ALWAYS:
            cmds.file(newFile=True, force=True)
