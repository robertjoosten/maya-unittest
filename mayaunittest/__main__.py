def main():
    import sys
    import atexit
    import unittest
    import maya.utils
    import maya.standalone

    maya.standalone.initialize()
    program = unittest.main(module=None, exit=False)

    maya.utils.processIdleEvents()
    maya.standalone.uninitialize()
    atexit._run_exitfuncs()

    ret_code = not program.result.wasSuccessful()
    sys.exit(ret_code)
    #os._exit(ret_code)  # sys.exit default to 0 at times.


if __name__ == "__main__":
    main()
