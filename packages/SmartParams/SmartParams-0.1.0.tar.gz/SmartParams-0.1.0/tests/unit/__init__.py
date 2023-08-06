import os
import unittest

_UNIT = bool(int(os.getenv('TEST_UNIT', default='1')))


@unittest.skipUnless(_UNIT, reason="Unit tests are disabled")
class UnitCase(unittest.TestCase):
    pass
