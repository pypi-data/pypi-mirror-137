import pathlib

from abc import ABC, abstractmethod
from typing import List, Optional

from data_to_model.models import ClassData

from .types import Collection


class DataParser(ABC):
    @abstractmethod
    async def from_file(
        self, file_path: pathlib.Path, root_class_name: Optional[str] = None, **kwargs
    ) -> List[ClassData]:
        pass

    @abstractmethod
    def from_collection(
        self, collection: Collection, root_class_name: str
    ) -> List[ClassData]:
        pass
