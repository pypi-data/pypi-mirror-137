# SmartParams
SmartParams is a lightweight Python framework that simplifies 
the development and configuration of research 
and other complex applications.

# Installation
Run `pip install smartparams`.

# Basic usage
```python
# examples/basic/script.py
from dataclasses import dataclass

from smartparams import Smart


@dataclass
class Params:
    value1: str
    value2: str


def main(smart: Smart[Params]) -> None:
    params = smart()

    print('value1', params.value1)
    print('value2', params.value2)


if __name__ == '__main__':
    Smart(Params).run(
        function=main,
    )
```

Run script `python -m examples.basic.script -s value1=one -s value2=two`.

The script can also be configured from a file. 
First create the template file manually or via

`python -m examples.basic.script --path examples/basic/params.yaml --dump`, 

then edit the file and set the appropriate values
```yaml
# params.yaml
value1: one
value2: two
```
finally, run script `python -m examples.basic.script --path examples/basic/params.yaml`.
