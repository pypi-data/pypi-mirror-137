from dataclasses import dataclass

from data_to_model.name_formatters import SnakeCaseFormatter


@dataclass()
class ClassField:
    original_name: str
    type: str

    @property
    def name(self) -> str:
        formatter = SnakeCaseFormatter(self.original_name)
        return formatter.format()
