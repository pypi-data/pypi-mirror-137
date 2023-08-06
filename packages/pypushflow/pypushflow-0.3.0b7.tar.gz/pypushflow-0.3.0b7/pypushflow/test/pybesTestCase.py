import unittest
import os


class PyBesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.environ[
            "PYPUSHFLOW_MONGOURL"
        ] = "mongodb://pybes:pybes@linsvensson.esrf.fr:27017/pybes"
        os.environ["PYPUSHFLOW_CREATOR"] = "PyPushflowUnitTests"

    def tearDown(self) -> None:
        os.environ.pop("PYPUSHFLOW_MONGOURL", None)
        os.environ.pop("PYPUSHFLOW_CREATOR", None)
