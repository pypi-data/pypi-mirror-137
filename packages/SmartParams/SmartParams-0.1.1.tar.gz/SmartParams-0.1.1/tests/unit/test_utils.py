from pathlib import Path

from smartparams.utils import get_filepath, get_nested
from tests.unit import UnitCase


class TestGetNested(UnitCase):
    def setUp(self) -> None:
        self.dict = dict(arg1='arg1', arg2=['arg2'], arg3={'arg31': 'a31', 'arg32': 'a32'})

    def test_nested(self) -> None:
        name = 'arg3.arg31'

        dictionary, key = get_nested(dictionary=self.dict, name=name)

        self.assertEqual('arg31', key)
        self.assertTupleEqual((('arg31', 'a31'), ('arg32', 'a32')), tuple(dictionary.items()))

    def test_nested__not_in_dictionary(self) -> None:
        name = 'missing.any'

        self.assertRaises(KeyError, get_nested, dictionary=self.dict, name=name)

    def test_nested__ensure_key_exists(self) -> None:
        name = 'arg3.missing'

        self.assertRaises(
            KeyError,
            get_nested,
            dictionary=self.dict,
            name=name,
            ensure_key_exists=True,
        )

    def test_nested__not_is_dictionary(self) -> None:
        name = 'arg3.arg31.a31'

        self.assertRaises(ValueError, get_nested, dictionary=self.dict, name=name)

    def test_nested__create_missing_directories(self) -> None:
        name = 'arg3.missing.key'

        dictionary, key = get_nested(
            dictionary=self.dict,
            name=name,
            create_missing_directories=True,
        )

        self.assertIsInstance(dictionary, dict)
        self.assertFalse(bool(dictionary))
        self.assertEqual('key', key)


class TestGetFilepath(UnitCase):
    def test_get_filepath(self) -> None:
        test_cases = (
            (None, None, None, 'none_none'),
            ('arg_file.yaml', None, 'arg_file.yaml', 'rel_none'),
            (None, 'cli_file.yaml', 'cli_file.yaml', 'none_rel'),
            ('/arg_file.yaml', None, '/arg_file.yaml', 'abs_none'),
            (None, '/cli_file.yaml', '/cli_file.yaml', 'none_abs'),
            ('/arg_file.yaml', 'cli_file.yaml', 'cli_file.yaml', 'abs_rel'),
            ('arg_file.yaml', '/cli_file.yaml', '/cli_file.yaml', 'rel_abs'),
            ('arg_file.yaml', 'cli_file.yaml', 'cli_file.yaml', 'rel_rel'),
            ('/arg_file.yaml', '/cli_file.yaml', '/cli_file.yaml', 'abs_abs'),
            ('/', None, '/params.yaml', 'dir_none'),
            ('/', 'cli_file.yaml', '/cli_file.yaml', 'dir_rel'),
            ('/home', '/cli_file.yaml', '/cli_file.yaml', 'dir_abs'),
            (None, '/home', '/home', 'none_dir'),
            ('cli_file.yaml', '/', '/', 'rel_dir'),
            ('/home/cli_file.yaml', '/', '/', 'abs_dir'),
            ('/home', '/', '/', 'dir_dir'),
        )

        for arg, cli, expected, msg in test_cases:
            with self.subTest(msg=msg):
                arg_path = Path(arg) if arg is not None else arg
                cli_path = Path(cli) if cli is not None else cli

                actual = get_filepath(arg_path, cli_path)

                if expected is None:
                    self.assertIsNone(actual)
                else:
                    self.assertEqual(Path(expected), actual)
