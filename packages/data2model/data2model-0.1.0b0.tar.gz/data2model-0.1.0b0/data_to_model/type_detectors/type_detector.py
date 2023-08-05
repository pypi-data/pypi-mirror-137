from typing import Set

from .types import SimpleType


class TypeNames:
    INTEGER = "int"
    FLOAT = "float"
    STRING = "str"
    BOOLEAN = "bool"
    NONE = "NoneType"
    OPTIONAL = "Optional"
    UNIOUN = "Union"


class TypeDetector:
    @staticmethod
    def from_value(value: SimpleType) -> str:

        if isinstance(value, bool):
            return TypeNames.BOOLEAN

        if value is None or value == "":
            return TypeNames.NONE

        if isinstance(value, int):
            return TypeNames.INTEGER

        if isinstance(value, float):
            return TypeNames.FLOAT

        if isinstance(value, str):
            return TypeDetector.from_string(value)

        raise TypeError(f"Expected SimpleType, got {type(value)}")

    @staticmethod
    def from_set(types: Set[str]) -> str:
        if len(types) == 1:
            t = types.pop()
            if t == TypeNames.NONE:
                return TypeNames.OPTIONAL
            return t

        if len(types) == 2 and TypeNames.NONE in types:
            t = [i for i in types if i != TypeNames.NONE][0]
            return f"Optional[{t}]"

        types_string = ", ".join(sorted([t for t in types if t != TypeNames.NONE]))
        union = f"{TypeNames.UNIOUN}[{types_string}]"

        if TypeNames.NONE in types:
            return f"{TypeNames.OPTIONAL}[{union}]"
        return union

    @staticmethod
    def from_string(value: str) -> str:
        if value.isdigit():
            return TypeNames.INTEGER

        try:
            float(value)
            return TypeNames.FLOAT
        except ValueError:
            return TypeNames.STRING
