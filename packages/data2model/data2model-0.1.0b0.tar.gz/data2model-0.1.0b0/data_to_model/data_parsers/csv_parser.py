import pathlib

from collections import defaultdict
from typing import AsyncGenerator, Dict, List, Optional, Set

import aiofiles

from aiocsv import AsyncDictReader
from data_to_model.data_parsers.data_parser import DataParser
from data_to_model.models import ClassData, ClassField
from data_to_model.name_formatters import CamelCaseFormatter
from data_to_model.type_detectors import TypeDetector

from .types import Collection


class CsvDataParser(DataParser):
    async def from_file(
        self,
        file_path: pathlib.Path,
        root_class_name: Optional[str] = None,
        **kwargs,
    ) -> List[ClassData]:
        delimiter = kwargs.get("delimiter", ",")
        all_types = defaultdict(set)

        type_detector = TypeDetector()
        async for row in self.read_csv(file_path, delimiter):
            for k, v in row.items():
                detected_type = type_detector.from_value(v)
                all_types[k].add(detected_type)

        fields = self.get_fields_from_types(all_types)

        if root_class_name is None:
            name_formatter = CamelCaseFormatter(file_path.stem)
            root_class_name = name_formatter.format()

        return [ClassData(root_class_name, fields)]

    def from_collection(
        self, collection: Collection, root_class_name: str
    ) -> List[ClassData]:
        all_types = defaultdict(set)
        type_detector = TypeDetector()
        for row in collection:
            for k, v in row.items():
                detected_type = type_detector.from_value(v)
                all_types[k].add(detected_type)

        fields = self.get_fields_from_types(all_types)

        return [ClassData(root_class_name, fields)]

    @staticmethod
    def get_fields_from_types(all_types: Dict[str, Set[str]]) -> List[ClassField]:
        types = {k: TypeDetector.from_set(v) for k, v in all_types.items()}
        fields = [ClassField(original_name=k, type=v) for k, v in types.items()]
        return fields

    @staticmethod
    async def read_csv(
        file_path: pathlib.Path, delimiter: str = ","
    ) -> AsyncGenerator[Dict[str, str], None]:
        delimiter = "," if delimiter is None else delimiter
        async with aiofiles.open(
            file_path, mode="r", encoding="utf-8", newline=""
        ) as f:
            async for row in AsyncDictReader(f, delimiter=delimiter):
                yield row
