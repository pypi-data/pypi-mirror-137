import os
import unittest

_BENCHMARK = bool(int(os.getenv('TEST_BENCHMARK', default='0')))


@unittest.skipUnless(_BENCHMARK, reason="Benchmark tests are disabled")
class BenchmarkCase(unittest.TestCase):
    pass
