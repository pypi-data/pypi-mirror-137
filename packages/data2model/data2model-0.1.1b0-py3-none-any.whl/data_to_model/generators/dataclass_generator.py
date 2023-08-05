from typing import List

from data_to_model.generators.base_generator import BaseGenerator
from data_to_model.models.data_class_model import DataClassModel

from .types import ClassData, ClassField


class DataClassGenerator(BaseGenerator):
    def generate_file_content(self) -> DataClassModel:
        self.content.append("from dataclasses import dataclass")
        self._add_typing_imports()

        for class_ in self.classes:
            self._add_class_content(class_)

        content = "\n".join(self.content)
        content += "\n\n"
        return DataClassModel(content)

    def _add_typing_imports(self) -> None:
        all_types = ["Dict", "Any"]
        for class_ in self.classes:
            all_types.extend(list(class_.get_types_for_import()))
        import_types = sorted(list(all_types))
        self.content.append(f"from typing import {', '.join(import_types)}\n\n")

    def _add_class_content(self, class_: ClassData) -> None:
        self.content.append(f"@dataclass\nclass {class_.name}:")
        self._add_fields_data(class_.fields)
        self._add_methods(class_)

    def _add_fields_data(self, fields: List[ClassField]) -> None:
        for field in fields:
            self.content.append(f"    {field.name}: {field.type}")

    def _add_methods(self, class_: ClassData) -> None:
        self._add_from_dict_method(class_)
        self._add_to_dict_method(class_)

    def _add_from_dict_method(self, class_: ClassData) -> None:
        self.content.append("\n    @classmethod")
        self.content.append(
            f'    def from_dict(cls, data: Dict[str, Any]) -> "{class_.name}":'
        )
        for field in class_.fields:
            getter = self.generate_dict_getter(field)
            self.content.append(f"        {getter}")

        return_statements = ", ".join([f"{i.name}={i.name}" for i in class_.fields])
        self.content.append(f"        return cls({return_statements})")

    def _add_to_dict_method(self, class_: ClassData) -> None:
        self.content.append("\n    def to_dict(self) -> Dict[str, Any]:")
        to_dict_template = '"{original_name}": self.{name}'
        return_statements = ", ".join(
            to_dict_template.format(original_name=i.original_name, name=i.name)
            for i in class_.fields
        )
        return_statements = "        return {" + return_statements + "}"
        self.content.append(return_statements)

    @staticmethod
    def generate_dict_getter(field: ClassField) -> str:
        types = {"str", "int", "float"}
        if field.type not in types:
            return f'{field.name} = data["{field.original_name}"]'

        return f'{field.name} = {field.type}(data["{field.original_name}"])'
