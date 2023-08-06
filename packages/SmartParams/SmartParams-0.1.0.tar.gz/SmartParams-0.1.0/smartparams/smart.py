import argparse
import inspect
from pathlib import Path
from pydoc import locate
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    cast,
    get_args,
    get_origin,
)

import yaml

_T = TypeVar("_T")


class Smart(Generic[_T]):
    NAME = "Smart"
    KEYWORD = "class"

    def __init__(self, _class: Optional[Type[_T]] = None, /, **params: Any) -> None:
        self._class = _class
        self._params = params

    @property
    def type(self) -> Optional[Type[_T]]:
        return self._class

    @property
    def params(self) -> dict[str, Any]:
        return self._params.copy()

    def __call__(self, *args: Any, **kwargs: Any) -> _T:
        if self._class is None:
            raise AttributeError("Class is not set.")

        return self._class(*args, **self._instantiate_dict(self._params), **kwargs)

    def __str__(self) -> str:
        if self._class is None:
            return f"{self.NAME}({str(self._params)})"

        params = ", ".join((f"{k}={v}" for k, v in self._params.items()))
        return f"{self._class.__name__}:{self.NAME}({params})"

    def __repr__(self) -> str:
        return str(self)

    def keys(self) -> list[str]:
        return list(self._params)

    def flatten_keys(self) -> list[str]:
        return self._flatten_keys(self._params)

    def init(self, name: str) -> Any:
        dictionary, key = self._get_nested(name)
        dictionary[key] = obj = self._instantiate(dictionary[key])
        return obj

    def get(self, name: str) -> Any:
        dictionary, key = self._get_nested(name, ensure_key_exists=True)
        return dictionary[key]

    def set(self, name: str, value: Any) -> Any:
        dictionary, key = self._get_nested(name, create_missing_directories=True)
        dictionary[key] = value
        return value

    def pop(self, name: str) -> Any:
        dictionary, key = self._get_nested(name, ensure_key_exists=True)
        return dictionary.pop(key)

    def map(self, name: str, function: Callable) -> Any:
        dictionary, key = self._get_nested(name, ensure_key_exists=True)
        dictionary[key] = value = function(dictionary[key])
        return value

    def update(self, params: dict[str, Any]) -> 'Smart':
        param: Smart = Smart(**params)
        for key in param.flatten_keys():
            self.set(key, param.get(key))
        return self

    def update_from(self, path: Path) -> 'Smart':
        if path.suffix in ('.yml', '.yaml'):
            with path.open() as stream:
                self.update(yaml.safe_load(stream))
        else:
            raise ValueError(f"File extension '{path.suffix}' is not supported.")

        return self

    def save_to(self, path: Path) -> 'Smart':
        if path.suffix in ('.yml', '.yaml'):
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w") as stream:
                yaml.safe_dump(
                    data=self.representation(),
                    stream=stream,
                    sort_keys=False,
                )
        else:
            raise ValueError(f"File extension '{path.suffix}' is not supported.")

        return self

    def run(
        self,
        function: Optional[Callable] = None,
        path: Optional[Path] = None,
        dump: bool = False,
        keys: bool = False,
    ) -> 'Smart':
        cli_path, dump, keys = self._parse_arguments(
            dump=dump,
            keys=keys,
        )

        filepath = self._get_filepath(
            arg_path=path,
            cli_path=cli_path,
        )

        if dump:
            if not filepath:
                raise ValueError("Missing destination filepath.")
            self.save_to(filepath)
        else:
            if filepath:
                self.update_from(filepath)

            if keys:
                print("\n".join(f"- {key}" for key in self.flatten_keys()))
            elif function is None:
                self()
            else:
                function(self)

        return self

    def representation(self) -> dict[str, Any]:
        return self._representation(self._class)

    @staticmethod
    def _parse_arguments(dump: bool, keys: bool) -> tuple[Optional[Path], bool, bool]:
        parser = argparse.ArgumentParser()
        parser.add_argument('--path', type=Path)
        parser.add_argument('--dump', default=dump, action='store_true')
        parser.add_argument('--keys', default=keys, action='store_true')
        args = parser.parse_args()
        return args.path, args.dump, args.keys

    @staticmethod
    def _get_filepath(arg_path: Optional[Path], cli_path: Optional[Path]) -> Optional[Path]:
        if arg_path is None:
            return cli_path

        if arg_path.is_dir():
            if cli_path is None:
                return arg_path.joinpath('params.yaml')

            if cli_path.is_absolute():
                return cli_path

            return arg_path.joinpath(cli_path)

        if cli_path is not None:
            return cli_path

        return arg_path

    def _flatten_keys(self, obj: Any, prefix: str = "") -> list[str]:
        if not isinstance(obj, dict):
            return [prefix]

        keys = []
        for k, v in obj.items():
            if prefix:
                k = f"{prefix}.{k}"
            keys.extend(self._flatten_keys(v, k))
        return keys

    def _get_nested(
        self,
        name: str,
        create_missing_directories: bool = False,
        ensure_key_exists: bool = False,
    ) -> Any:
        dictionary = self._params
        *nested_keys, last_key = name.split('.')

        keys = []
        for k in nested_keys:
            keys.append(k)
            if k not in dictionary:
                if create_missing_directories:
                    dictionary[k] = dict()
                else:
                    raise KeyError(f"Param {'.'.join(keys)} is not in dictionary.")

            dictionary = dictionary[k]
            if not isinstance(dictionary, dict):
                raise ValueError(f"Param {'.'.join(keys)} is not dictionary.")

        if ensure_key_exists and last_key not in dictionary:
            raise KeyError(f"Param {'.'.join(keys)} is not in dictionary.")

        return dictionary, last_key

    def _instantiate(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            if self.KEYWORD in obj:
                return self._instantiate_class(obj)
            return self._instantiate_dict(obj)
        if isinstance(obj, list):
            return self._instantiate_list(obj)
        return obj

    def _instantiate_dict(self, dictionary: dict[str, Any]) -> dict[str, Any]:
        return {k: self._instantiate(v) for k, v in dictionary.items()}

    def _instantiate_list(self, lst: list[Any]) -> list[Any]:
        return [self._instantiate(o) for o in lst]

    def _instantiate_class(self, dictionary: dict[str, Any]) -> Any:
        kwargs = dictionary.copy()
        class_name = kwargs.pop(self.KEYWORD)
        class_name, _, option = class_name.partition(':')
        if class_name == self.NAME:
            return Smart(**kwargs)

        cls = cast(Optional[Type[_T]], locate(class_name))
        if cls is None:
            raise ValueError(f"Class '{class_name}' does not exist.")

        if option:
            if option == self.NAME:
                return Smart(cls, **kwargs)
            else:
                raise ValueError(f"Option '{option}' is not supported.")
        else:
            return cls(**kwargs)

    def _representation(self, obj: Any) -> dict[str, Any]:
        is_class = inspect.isclass(obj)
        if is_class:
            obj = obj.__init__

        representation: dict[str, Any] = dict()
        signature = inspect.signature(obj)

        for name, param in signature.parameters.items():
            if name != 'self' and param.kind in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            ):
                representation[name] = self._param_representation(
                    annotation=param.annotation,
                    default=param.default,
                )

        return representation

    def _param_representation(self, annotation: Any, default: Any) -> Any:
        if annotation is Smart:
            return self._class_representation(self.NAME)

        if get_origin(annotation) is Smart:
            suffix = f':{self.NAME}'

            if default is not inspect.Parameter.empty:
                param_type = default.type
                param_name = inspect.formatannotation(param_type) + suffix
                return self._class_representation(
                    name=self.NAME if param_type is None else param_name,
                    annotation=param_type,
                )

            param_type, *_ = get_args(annotation)
            return self._class_representation(
                name=inspect.formatannotation(param_type) + suffix,
                annotation=param_type,
            )

        if annotation is not inspect.Parameter.empty and isinstance(annotation, type):
            if annotation in (bool, float, int, str):
                return annotation.__name__ + '?'

            if annotation is dict:
                return {}

            if annotation in (list, tuple):
                return []

            return self._class_representation(
                name=inspect.formatannotation(annotation),
                annotation=annotation,
            )

        if default is not inspect.Parameter.empty and isinstance(default, (bool, float, int, str)):
            return default

        return '?'

    def _class_representation(self, name: str, annotation: Optional[Any] = None) -> dict[str, Any]:
        return {
            self.KEYWORD: name,
            **(dict() if annotation is None else self._representation(annotation)),
        }
