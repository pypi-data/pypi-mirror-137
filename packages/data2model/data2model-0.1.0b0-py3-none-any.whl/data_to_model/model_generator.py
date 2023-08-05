import pathlib

from typing import List, Optional, Union

from data_to_model.data_parsers import DataParser, DataParserFactory
from data_to_model.data_parsers.types import Collection, SupportedDataTypes
from data_to_model.generators.base_generator import BaseGenerator
from data_to_model.generators.factory import GeneratorFactory
from data_to_model.generators.types import SupportedDataClasses
from data_to_model.models import ClassData
from data_to_model.models.data_class_model import DataClassModel


Data = Union[pathlib.Path, Collection]


class ModelGenerator:
    def __init__(
        self,
        data: Data,
        *,
        py_dataclass_type: SupportedDataClasses = SupportedDataClasses.PythonDataClass,
        data_type: Optional[SupportedDataTypes] = None,
        root_class_name: Optional[str] = None,
        csv_delimiter: Optional[str] = None,
    ):
        self.data = data
        self.py_dataclass_type = py_dataclass_type
        self.data_type = data_type
        self.root_class_name = root_class_name
        self.csv_delimiter = csv_delimiter

    async def get_model(self) -> DataClassModel:
        data = await self._get_data()
        model = self._get_model(data)
        return model

    async def _get_data(self) -> List[ClassData]:
        data_parser = self._get_data_parser()
        is_path = isinstance(self.data, pathlib.Path)
        if is_path:
            data = await data_parser.from_file(self.data, delimiter=self.csv_delimiter)  # type: ignore
        else:
            if self.root_class_name is None:
                raise ValueError(
                    "root_class_name must be specified if data is not a path"
                )
            data = data_parser.from_collection(self.data, self.root_class_name)  # type: ignore
        return data

    def _get_model(self, data: List[ClassData]) -> DataClassModel:
        dc_generator = self._get_data_class_generator(data)
        return dc_generator.generate_file_content()

    def _get_data_parser(self) -> DataParser:
        if not isinstance(self.data, pathlib.Path) and self.data_type is None:
            raise ValueError("data_type must be specified if data is not a path")
        return (
            DataParserFactory.get_parser(self.data)  # type: ignore
            if self.data_type is None
            else DataParserFactory.get_parser(self.data_type)
        )

    def _get_data_class_generator(self, classes: List[ClassData]) -> BaseGenerator:
        return GeneratorFactory.get_generator(self.py_dataclass_type, classes)  # type: ignore
