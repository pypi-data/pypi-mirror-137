from pathlib import Path
from unittest.mock import Mock, patch

from smartparams.smart import Smart
from tests.unit import UnitCase


class Class:
    def __init__(self, arg1: str, arg2: int = 5) -> None:
        self.arg1 = arg1
        self.arg2 = arg2


class TestSmartInitCase(UnitCase):
    def setUp(self) -> None:
        self.smart = Smart(Class, arg1='arg1', arg2=10)

    def test_type(self) -> None:
        smart_type = self.smart.type

        self.assertIs(smart_type, Class)

    def test_type__none(self) -> None:
        smart: Smart = Smart()

        smart_type = smart.type

        self.assertIs(smart_type, None)

    def test_params(self) -> None:
        params = self.smart.params

        self.assertIsInstance(params, dict)
        self.assertTupleEqual((('arg1', 'arg1'), ('arg2', 10)), tuple(params.items()))
        self.assertIsNot(self.smart._params, params)
        self.assertTupleEqual(tuple(self.smart._params.items()), tuple(params.items()))

    def test_call(self) -> None:
        obj = self.smart()

        self.assertIsInstance(obj, Class)
        self.assertEqual('arg1', obj.arg1)
        self.assertEqual(10, obj.arg2)

    def test_call__with_params(self) -> None:
        smart = Smart(Class)

        obj = smart('a1', arg2=15)

        self.assertIsInstance(obj, Class)
        self.assertEqual('a1', obj.arg1)
        self.assertEqual(15, obj.arg2)

    def test_call__with_duplicated_params(self) -> None:
        smart = Smart(Class, arg1='arg1')

        self.assertRaises(TypeError, smart, 'a1')

    def test_call__without_class(self) -> None:
        smart: Smart = Smart()

        self.assertRaises(AttributeError, smart)

    def test_str(self) -> None:
        string = str(self.smart)

        self.assertEqual("Class:Smart(arg1=arg1, arg2=10)", string)

    def test_str__without_class(self) -> None:
        smart: Smart = Smart(arg1='arg1', arg2=10)

        string = str(smart)

        self.assertEqual("Smart({'arg1': 'arg1', 'arg2': 10})", string)


class TestSmartAccessCase(UnitCase):
    def setUp(self) -> None:
        self.smart: Smart = Smart(arg1='arg1', arg2=['arg2'], arg3={'arg31': 'a31', 'arg32': 'a32'})

    def test_keys(self) -> None:
        keys = self.smart.keys()

        self.assertTupleEqual(('arg1', 'arg2', 'arg3'), tuple(keys))

    def test_get(self) -> None:
        value = self.smart.get('arg1')

        self.assertEqual('arg1', value)

    def test_get__nested(self) -> None:
        value = self.smart.get('arg3.arg31')

        self.assertEqual('a31', value)

    def test_set(self) -> None:
        new_value = 'argument3'

        value = self.smart.set('arg3', new_value)

        self.assertEqual(new_value, value)
        self.assertEqual(new_value, self.smart.params['arg3'])

    def test_set__nested(self) -> None:
        new_value = 'argument31'

        value = self.smart.set('arg3.arg31', new_value)

        self.assertEqual('argument31', value)
        self.assertEqual('argument31', self.smart.params['arg3']['arg31'])
        self.assertEqual('a32', self.smart.params['arg3']['arg32'])

    def test_pop(self) -> None:
        value = self.smart.pop('arg2')

        self.assertEqual(['arg2'], value)
        self.assertFalse('arg2' in self.smart.params)

    def test_pop__nested(self) -> None:
        value = self.smart.pop('arg3.arg31')

        self.assertEqual('a31', value)
        self.assertFalse('arg3' in self.smart.params['arg3'])

    def test_map(self) -> None:
        value = self.smart.map('arg2', set)

        self.assertIsInstance(value, set)
        self.assertSetEqual({'arg2'}, value)
        self.assertSetEqual({'arg2'}, self.smart.params['arg2'])

    def test_map__nested(self) -> None:
        function = Mock(return_value='argument31')

        value = self.smart.map('arg3.arg31', function)

        self.assertEqual('argument31', value)
        self.assertEqual('argument31', self.smart.params['arg3']['arg31'])
        self.assertEqual('a32', self.smart.params['arg3']['arg32'])

    def test_update(self) -> None:
        self.smart.update({'arg3': {'arg31': 'argument31'}, 'arg4': 'argument4'})

        self.assertTrue('arg1' in self.smart.params)
        self.assertTrue('arg2' in self.smart.params)
        self.assertTrue('arg3' in self.smart.params)
        self.assertTrue('arg4' in self.smart.params)
        self.assertEqual('arg1', self.smart.params['arg1'])
        self.assertListEqual(['arg2'], self.smart.params['arg2'])
        self.assertEqual('argument31', self.smart.params['arg3']['arg31'])
        self.assertEqual('a32', self.smart.params['arg3']['arg32'])
        self.assertEqual('argument4', self.smart.params['arg4'])

    def test_flatten_keys(self) -> None:
        value = self.smart.flatten_keys()

        self.assertListEqual(['arg1', 'arg2', 'arg3.arg31', 'arg3.arg32'], value)

    def test__flatten_keys(self) -> None:
        dictionary = {'1': {'1': 'a'}, '2': 'a'}
        prefix = 'prefix'

        value = self.smart._flatten_keys(dictionary, prefix)

        self.assertListEqual(['prefix.1.1', 'prefix.2'], value)


class TestSmartRunCase(UnitCase):
    def setUp(self) -> None:
        self.smart = Smart(Class, arg1='arg1', arg2=10)

    @patch('smartparams.smart.get_filepath', Mock(return_value=Path('/file.yaml')))
    @patch('smartparams.smart.parse_arguments', Mock())
    def test_run_dump(self) -> None:
        self.smart._update_from_list = Mock()  # type: ignore
        self.smart.save = Mock()  # type: ignore

        self.smart.run(path=Path('/file.yaml'), dump=True)

        self.smart.save.assert_called_once_with(Path('/file.yaml'))

    @patch('smartparams.smart.get_filepath', Mock(return_value=None))
    @patch('smartparams.smart.parse_arguments', Mock())
    @patch('smartparams.smart.print')
    def test_run_dump__none_path(self, print_mock: Mock) -> None:
        self.smart._update_from_list = Mock()  # type: ignore
        self.smart.save = Mock()  # type: ignore

        self.smart.run(path=Path('/file.yaml'), dump=True)

        print_mock.assert_called_once_with('arg1: str???\narg2: 5\n')
