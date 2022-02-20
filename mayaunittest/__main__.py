def main():
    import os
    import sys
    import unittest
    import maya.standalone

    os.environ["MAYA_NO_STANDALONE_ATEXIT"] = "1"
    maya.standalone.initialize()
    program = unittest.main(module=None, exit=False)
    maya.standalone.uninitialize()

    ret_code = not program.result.wasSuccessful()
    sys.exit(ret_code)
    #os._exit(ret_code)  # sys.exit default to 0 at times.


if __name__ == "__main__":
    main()
