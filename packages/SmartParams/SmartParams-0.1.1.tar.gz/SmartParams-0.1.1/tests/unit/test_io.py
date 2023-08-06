from smartparams.io import to_string
from tests.unit import UnitCase


class TestToString(UnitCase):
    def test_yaml_list(self) -> None:
        lst = [None, True, {'1': 2, '3': 4}]

        string = to_string(lst, 'yaml')

        self.assertEqual("- null\n- true\n- '1': 2\n  '3': 4\n", string)

    def test_yaml_dict(self) -> None:
        dictionary = {'1': [True, False], 3: None}

        string = to_string(dictionary, 'yaml')

        self.assertEqual("'1':\n- true\n- false\n3: null\n", string)

    def test_yaml_error(self) -> None:
        self.assertRaises(ValueError, to_string, dict(), 'unknown')
