def main():
    import sys
    import unittest
    import maya.standalone

    maya.standalone.initialize()
    program = unittest.main(module=None, exit=False)
    maya.standalone.uninitialize()

    sys.exit(not program.result.wasSuccessful())


if __name__ == "__main__":
    main()
