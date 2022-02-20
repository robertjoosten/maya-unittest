import os
from maya import cmds
from mayaunittest import MayaTestCase
from mayaunittest.constants import TEMP_DIRECTORY


class TestMayaTestCase(MayaTestCase):
    plugin = "fbxmaya"

    def test_load_plugin(self):
        self.load_plugin(self.plugin)

        loaded = cmds.pluginInfo(self.plugin, query=True, loaded=True)
        self.assertTrue(loaded)

    def test_unload_plugins(self):
        if cmds.pluginInfo(self.plugin, query=True, loaded=True):
            cmds.unloadPlugin(self.plugin)

        self.load_plugin(self.plugin)
        self.unload_plugins()

        loaded = cmds.pluginInfo(self.plugin, query=True, loaded=True)
        self.assertFalse(loaded)

    def test_get_temp_path(self):
        temp_path = self.get_temp_path("test.json")
        self.assertEqual(temp_path, os.path.join(TEMP_DIRECTORY, "test.json"))

        with self.assertRaises(RuntimeError):
            self.get_temp_path()

    def test_delete_temp_directory(self):
        temp_path = self.get_temp_path("test.json")
        with open(temp_path, "w") as f:
            f.write("test")

        self.delete_temp_directory()
        self.assertFalse(os.path.exists(temp_path))
