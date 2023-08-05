import pathlib

from typing import Union

from .data_parser import DataParser
from .types import SupportedDataTypes


class DataParserFactory:
    @staticmethod
    def get_parser(
        data_type: Union[SupportedDataTypes, pathlib.Path],
    ) -> DataParser:
        if isinstance(data_type, pathlib.Path):
            data_type = SupportedDataTypes.from_path(data_type)

        if data_type == SupportedDataTypes.CSV:
            from .csv_parser import CsvDataParser

            return CsvDataParser()
        else:
            raise ValueError("Data type not supported")
