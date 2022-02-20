def main():
    import os
    import unittest
    import maya.utils
    import maya.standalone

    maya.standalone.initialize()
    program = unittest.main(module=None, exit=False)

    maya.utils.processIdleEvents()
    maya.standalone.uninitialize()

    ret_code = not program.result.wasSuccessful()
    os._exit(ret_code)  # sys.exit default to 0 at times.


if __name__ == "__main__":
    main()
