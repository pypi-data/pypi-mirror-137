# config_manager

![Tests](https://github.com/evjeny/config_manager/actions/workflows/python-app.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/evjeny/config_manager)
[![PyPI](https://img.shields.io/badge/PyPI-config_manager_evjeny-blue)](https://pypi.org/project/config-manager-evjeny)

Configuration manager for parsing from different sources

## Installation

```bash
python -m pip install config-manager-evjeny
```

## Usage

Create class with config variables and inherit it from `config_manager.config.Config`.
You can define variables and their types or even define values.
Then we can parse variables from different sources.
For example, this is [example_parser.py](example_parser.py):

```python
from config_manager.config import Config
from config_manager.variable_parsers import ListType


class TestConfig(Config):
    """Config example with some variables of different types"""

    name: str
    age: int
    is_useful: bool = False
    parts: ListType[float]


my_config = TestConfig() \
    .parse_env(prefix="test_config_") \
    .parse_json(json_path="test_config.json") \
    .parse_arguments("TestConfig parser")

print(my_config)
```

If we run it:

```bash
test_config_age=33 python example_parser.py \
  --name hello \
  --is_useful false \
  --parts "[0.25, 0.5, 0.75]"
```

It will output something like and all the *primitive* types will be parsed correctly:

```
age = 33
is_useful = False
name = hello
parts = [0.25, 0.5, 0.75]
```

## Type details

### `str`, `int` and `float`

For `str`, `int` and `float` casting is the same as builtin functions.

### `bool`

Generally all not empty containers (even string `"false"`)
cast to `bool` would return `True`.

Thus, there is a `BoolParser` that casts value to `True` in one of these cases:
* variable is subclass of `str` and it's value one of (in any case):
  * `"yes"`
  * `"true"`
  * `"1"`
  * `"on"`
* in other cases default `bool` call used

```python
from config_manager.variable_parsers import BoolParser

parser = BoolParser()

assert parser("yes") == True
assert parser("yES") == True
assert parser("tRuE") == True
assert parser("1") == True
assert parser("on") == True

assert parser("no") == False
assert parser("FaLsE") == False

assert parser(1.0) == True
assert parser(0.0) == False
assert parser(1) == True
assert parser(0) == False
assert parser(True) == True
assert parser(False) == False
```

### `ListType`

As it is impossible to get type from `typing.List[T]`
(plus this annotation removed in Python 3.9) there is a `ListType`.
It can be used with any parseable type, so every element will be cast
to target type. For example:

```python
from config_manager.variable_parsers import ListType

# shallow lists
assert ListType[int](["1", "2", "3"]) == [1, 2, 3]
assert ListType[str]([1.0, -213.5122, 52.123]) == ["1.0", "-213.5122", "52.123"]
assert ListType[int]("[1, 2, 3]") == [1, 2, 3]
```

All the parse sources provide different ways to define list, so there they are:
* in `predefine` and `json` case simply assign any python list to variable
* in `environment` and `argument` cases every list is parsed from string `[item_1, item_2, ...]`
