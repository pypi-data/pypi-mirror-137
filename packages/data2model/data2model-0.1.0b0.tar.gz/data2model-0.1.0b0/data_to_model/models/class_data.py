from typing import List, Set

from data_to_model.models.class_field import ClassField


class ClassData:
    types_for_import = {"Dict", "List", "Union", "Any", "Optional"}

    def __init__(self, name: str, fields: List[ClassField]):
        self.name = name
        self.fields = fields

    def __repr__(self) -> str:
        field_names = [field.name for field in self.fields]
        return f"ClassData(name={self.name}, fields={field_names})"

    def get_types_for_import(self) -> Set[str]:
        all_types = self.get_all_types()
        types_for_import = set()
        for type_ in all_types:
            for import_type in self.types_for_import:
                if import_type in type_:
                    types_for_import.add(import_type)
        return types_for_import

    def get_all_types(self) -> Set[str]:
        return {field.type for field in self.fields}
