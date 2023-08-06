import os
import unittest

_INTEGRATION = bool(int(os.getenv('TEST_INTEGRATION', default='0')))


@unittest.skipUnless(_INTEGRATION, reason="Integration tests are disabled")
class IntegrationCase(unittest.TestCase):
    pass
