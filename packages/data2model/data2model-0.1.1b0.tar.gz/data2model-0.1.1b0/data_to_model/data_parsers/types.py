import pathlib

from enum import Enum, auto
from typing import Any, Dict, List, Union

from data_to_model.type_detectors.types import SimpleType


CsvDataType = List[Dict[str, SimpleType]]
JsonDataType = Dict[str, Any]
Collection = Union[CsvDataType, Dict]


class SupportedDataTypes(Enum):
    CSV = auto()

    @classmethod
    def from_path(cls, path: pathlib.Path) -> "SupportedDataTypes":
        if path.suffix in {".csv", ".tsv", ".txt"}:
            return cls.CSV
        raise ValueError(f"Unsupported file type: {path.suffix}")
