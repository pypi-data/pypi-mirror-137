from pathlib import Path
from typing import Any, Optional


def get_filepath(
    arg_path: Optional[Path] = None,
    cli_path: Optional[Path] = None,
    default_params_filename: str = 'params.yaml',
) -> Optional[Path]:
    if arg_path is None:
        return cli_path

    if arg_path.is_dir():
        if cli_path is None:
            return arg_path.joinpath(default_params_filename)

        if cli_path.is_absolute():
            return cli_path

        return arg_path.joinpath(cli_path)

    if cli_path is not None:
        return cli_path

    return arg_path


def get_nested(
    dictionary: dict[str, Any],
    name: str,
    create_missing_directories: bool = False,
    ensure_key_exists: bool = False,
    separator: str = '.',
) -> tuple[dict[str, Any], str]:
    *nested_keys, last_key = name.split(separator)

    key_list = list()
    for key in nested_keys:
        key_list.append(key)
        if key not in dictionary:
            if create_missing_directories:
                dictionary[key] = dict()
            else:
                raise KeyError(f"Param {separator.join(key_list)} is not in dictionary.")

        dictionary = dictionary[key]
        if not isinstance(dictionary, dict):
            raise ValueError(f"Param {separator.join(key_list)} is not dictionary.")

    if ensure_key_exists and last_key not in dictionary:
        raise KeyError(f"Param {separator.join(key_list)} is not in dictionary.")

    return dictionary, last_key
