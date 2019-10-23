import sys
if sys.argv[1] == "test":
    from .test_all import unittest
    unittest.main()

from .pytris import main
main()
