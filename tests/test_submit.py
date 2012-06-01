import sys
import legit
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
    
class SubmitTest(unittest.TestCase):
    pass