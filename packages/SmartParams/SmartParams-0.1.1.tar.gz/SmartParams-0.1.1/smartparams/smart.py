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
    Union,
    cast,
    get_args,
    get_origin,
)

import yaml
from yaml import YAMLError

from smartparams.cli import parse_arguments
from smartparams.io import load, save, to_string
from smartparams.utils import get_filepath, get_nested

_T = TypeVar("_T")


class Smart(Generic[_T]):
    name = "Smart"
    keyword = "class"
    self_keyword = 'self'
    missing_mark = '???'

    params_filename = 'params.yaml'
    print_format = 'yaml'

    key_separator = '.'
    param_separator = '='
    class_name_separator = ':'

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

        params = self._instantiate_dict(self._params)
        return self._class(*args, **params, **kwargs)

    def __str__(self) -> str:
        if self._class is None:
            return f"{self.name}({str(self._params)})"

        params = ", ".join((f"{k}={v}" for k, v in self._params.items()))
        return f"{self._class.__name__}:{self.name}({params})"

    def __repr__(self) -> str:
        return str(self)

    def keys(self) -> list[str]:
        return list(self._params)

    def flatten_keys(self) -> list[str]:
        return self._flatten_keys(self._params)

    def representation(self) -> dict[str, Any]:
        return self._representation(self._class)

    def init(self, name: str) -> Any:
        dictionary, key = get_nested(
            dictionary=self._params,
            name=name,
            separator=self.key_separator,
        )
        dictionary[key] = obj = self._instantiate(dictionary[key])
        return obj

    def get(self, name: str) -> Any:
        dictionary, key = get_nested(
            dictionary=self._params,
            name=name,
            ensure_key_exists=True,
            separator=self.key_separator,
        )
        return dictionary[key]

    def set(self, name: str, value: Any) -> Any:
        dictionary, key = get_nested(
            dictionary=self._params,
            name=name,
            create_missing_directories=True,
            separator=self.key_separator,
        )
        dictionary[key] = value
        return value

    def pop(self, name: str) -> Any:
        dictionary, key = get_nested(
            dictionary=self._params,
            name=name,
            ensure_key_exists=True,
            separator=self.key_separator,
        )
        return dictionary.pop(key)

    def map(self, name: str, function: Callable) -> Any:
        dictionary, key = get_nested(
            dictionary=self._params,
            name=name,
            ensure_key_exists=True,
            separator=self.key_separator,
        )
        dictionary[key] = value = function(dictionary[key])
        return value

    def update(self, source: Union[dict[str, Any], list[str], Path]) -> 'Smart':
        if isinstance(source, dict):
            self._update_from_dict(source)
        elif isinstance(source, list):
            self._update_from_list(source)
        elif isinstance(source, Path):
            self._update_from_path(source)
        else:
            raise TypeError(f"Source type '{type(source)}' is not supported.")

        return self

    def save(self, path: Path) -> 'Smart':
        save(
            data=self.representation(),
            path=path,
        )
        return self

    def run(
        self,
        function: Optional[Callable] = None,
        path: Optional[Path] = None,
        dump: bool = False,
        keys: bool = False,
    ) -> 'Smart':
        args = parse_arguments(
            dump_default=dump,
            keys_default=keys,
        )

        self._update_from_list(args.set)

        filepath = get_filepath(
            arg_path=path,
            cli_path=args.path,
            default_params_filename=self.params_filename,
        )

        if args.dump:
            if filepath:
                self.save(filepath)
            else:
                print(to_string(self.representation(), self.print_format))
        else:
            if filepath:
                self._update_from_path(filepath)

            if args.keys:
                print(to_string(self.flatten_keys(), self.print_format))
            elif function is None:
                self()
            else:
                function(self)

        return self

    def _update_from_dict(self, params: dict[str, Any]) -> None:
        param: Smart = Smart(**params)
        for key in param.flatten_keys():
            self.set(key, param.get(key))

    def _update_from_list(self, params_list: list[str]) -> None:
        for param in params_list:
            key, separator, raw_value = param.partition(self.param_separator)
            if not separator:
                raise ValueError(f"Param '{param}' does not contain '=' mark.")

            try:
                value = yaml.safe_load(raw_value)
            except YAMLError as e:
                raise ValueError(f"Param '{param}' has invalid value.") from e

            self.set(key, value)

    def _update_from_path(self, path: Path) -> None:
        self._update_from_dict(load(path))

    def _flatten_keys(self, obj: Any, prefix: str = "") -> list[str]:
        if not isinstance(obj, dict):
            return [prefix]

        keys = []
        for k, v in obj.items():
            if prefix:
                k = prefix + self.key_separator + k
            keys.extend(self._flatten_keys(v, k))

        return keys

    def _instantiate(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            if self.keyword in obj:
                return self._instantiate_class(obj)
            return self._instantiate_dict(obj)
        if isinstance(obj, list):
            return self._instantiate_list(obj)
        return obj

    def _instantiate_dict(self, dictionary: dict[str, Any]) -> dict[str, Any]:
        return {k: self._instantiate(v) for k, v in dictionary.items()}

    def _instantiate_list(self, lst: list[Any]) -> list[Any]:
        return [self._instantiate(el) for el in lst]

    def _instantiate_class(self, dictionary: dict[str, Any]) -> Any:
        kwargs = dictionary.copy()
        class_name = kwargs.pop(self.keyword)
        class_name, _, option = class_name.partition(self.class_name_separator)
        if class_name == self.name:
            return Smart(**kwargs)

        cls = cast(Optional[Type[_T]], locate(class_name))
        if cls is None:
            raise ValueError(f"Class '{class_name}' does not exist.")

        if option:
            if option == self.name:
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
            if name != self.self_keyword and param.kind in (
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
            return {
                self.keyword: self.name,
            }

        if get_origin(annotation) is Smart:
            suffix = self.class_name_separator + self.name

            if default is not inspect.Parameter.empty:
                param_type = default.type
                param_name = inspect.formatannotation(param_type) + suffix
                return {
                    self.keyword: self.name if param_type is None else param_name,
                    **self._representation(param_type),
                }

            param_type, *_ = get_args(annotation)
            return {
                self.keyword: inspect.formatannotation(param_type) + suffix,
                **self._representation(param_type),
            }

        if default is not inspect.Parameter.empty and isinstance(default, (bool, float, int, str)):
            return default

        if annotation is not inspect.Parameter.empty and isinstance(annotation, type):
            if annotation in (bool, float, int, str):
                return annotation.__name__ + self.missing_mark

            return {
                self.keyword: inspect.formatannotation(annotation),
                **self._representation(annotation),
            }

        return self.missing_mark
