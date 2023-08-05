from typing import List

from .base_generator import BaseGenerator
from .dataclass_generator import DataClassGenerator
from .types import ClassData, SupportedDataClasses


DATA_CLASSES = {SupportedDataClasses.PythonDataClass: DataClassGenerator}


class GeneratorFactory:
    @staticmethod
    def get_generator(
        data_class: SupportedDataClasses, classes: List[ClassData]
    ) -> BaseGenerator:
        try:
            return DATA_CLASSES[data_class](classes)
        except KeyError:
            raise NotImplementedError(f"{data_class} is not supported")
