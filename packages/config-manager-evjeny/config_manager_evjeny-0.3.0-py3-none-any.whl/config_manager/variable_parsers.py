"""This module provides some implementations of config variables' types"""

from typing import Dict, Any


class BoolParser:  # pylint: disable=too-few-public-methods
    """Parser for variables of type `bool`

    Will transform `str` variables with values
    "true", "yes", "1" and "on" to `True`, others to `False`.
    Will leave `bool` variables as they are.
    """

    _true_forms = {"true", "yes", "1", "on"}

    def __call__(self, value) -> bool:
        if isinstance(value, str):
            return value.lower() in self._true_forms
        return bool(value)


class BasicParser:  # pylint: disable=too-few-public-methods
    """Superclass for variable parsers"""

    _variable_parsers = {bool: BoolParser()}

    def __init__(self, additional_parsers: Dict[Any, Any] = None):
        if additional_parsers:
            self._variable_parsers.update(additional_parsers)

    def _parse_variable(self, variable_type, value):
        """Parse variable with known parser from `_variable_parsers` or with `variable_type` parser
        :param variable_type: type of variable from annotation
        :param value: value to parse
        :return: parsed value
        """
        variable_parser = self._variable_parsers.get(variable_type, variable_type)
        return variable_parser(value)


class ListType(list, BasicParser):
    """Config type for lists with items of same type

    Can be used as `variable: ListType[str]`

    Will transform string by splitting it with commas, for example:
    `ListType[int]("[1,2,3]") == [1, 2, 3]`

    Will transform list by converting all its elements to type, for example:
    `ListType[int](["1", "2", "3"]) == [1, 2, 3]`
    """

    def __init__(self, item_type):
        super().__init__()
        self.item_type = item_type

    def __class_getitem__(cls, item_type):
        list_object = super().__new__(ListType)
        list_object.__init__(item_type)
        return list_object

    def __hash__(self):
        return hash(f"ListType[{self.item_type}]")

    @staticmethod
    def empty_split(value: str, sep: str) -> list:
        """Splits string with separator

        If string is empty, then [] returned"""
        if value == "":
            return []
        return value.split(sep)

    def _cast_list(self, array: list):
        return [self._parse_variable(self.item_type, e) for e in array]

    def _cast_string(self, value: str):
        if not value.startswith("[") or not value.endswith("]"):
            raise Exception(
                f"Expected `str` list representation in brackets `[` and `]`, but got: `{value}`"
            )
        return self._cast_list(array=self.empty_split(value[1:-1], sep=","))

    def __call__(self, value):
        if isinstance(value, str):
            return self._cast_string(value)
        if isinstance(value, list):
            return self._cast_list(value)

        raise Exception(f"Can't cast type {type(value)} to list of {self.item_type}")
