# maya-unittest
Unittest subset for specific use in Maya. The main has been adjusted to 
initialize a standalone session of Maya. 

## Install
The package can be installed by running the install command on the setup.py
in the root of the package, the example below also shows how to run the test
suite to make sure everything is working as expected.
```
mayapy setup.py install
mayapy -m mayaunittest discover tests -v --pattern "test_*.py"
```

## Usage
Create tests specific for Maya using MayaTestCase, it contains utility 
functions for generating temporary file paths, loading plugins and settings 
for logging levels and file news. The options for file new are to disable it,
do it at class setup and teardown, or between each individual test which is 
the default.

```python
import os
import logging
from maya import cmds
from mayaunittest import MayaTestCase


class Testing(MayaTestCase):
    plugin = "my_custom_plugin"
    file_new = MayaTestCase.FILE_NEW_ALWAYS
    logging_level = logging.WARNING 

    def test_custom_plugin(self):
        self.load_plugin(self.plugin)
        loaded = cmds.pluginInfo(self.plugin, query=True, loaded=True)
        self.assertTrue(loaded)
    
    def test_file_save(self):
        file_path = self.get_temp_path("test.ma")
        cmds.rename(file_path)
        cmds.file(save=True, force=True, type="mayaAscii")
        self.assertTrue(os.path.exists(file_path))

```

These test can be located in a test directory within your Maya module/scripts.
From there they can be ran from the command line using the following command.

```
mayapy -m mayaunittest discover tests -v --pattern "test_*.py"
```