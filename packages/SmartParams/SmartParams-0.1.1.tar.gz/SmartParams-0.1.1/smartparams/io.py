from pathlib import Path
from typing import Any

import yaml


def to_string(data: Any, fmt: str) -> str:
    if fmt in ('yml', 'yaml'):
        return yaml.safe_dump(
            data=data,
            sort_keys=False,
        )

    raise ValueError(f"Format '{fmt}' is not supported.")


def save(data: dict[str, Any], path: Path) -> None:
    if path.suffix in ('.yml', '.yaml'):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as stream:
            yaml.safe_dump(
                data=data,
                stream=stream,
                sort_keys=False,
            )
    else:
        raise ValueError(f"File extension '{path.suffix}' is not supported.")


def load(path: Path) -> dict[str, Any]:
    if path.suffix in ('.yml', '.yaml'):
        with path.open() as stream:
            dictionary = yaml.safe_load(stream)
            if isinstance(dictionary, dict):
                return dictionary
            raise ValueError(f"File '{path}' does not contain a dictionary.")
    raise ValueError(f"File extension '{path.suffix}' is not supported.")
