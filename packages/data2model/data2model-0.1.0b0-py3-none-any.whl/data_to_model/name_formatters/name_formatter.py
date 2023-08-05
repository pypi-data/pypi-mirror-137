from abc import ABC, abstractmethod
from typing import List


class NameFormatter(ABC):
    def __init__(self, original_name: str):
        self.original_name = original_name
        self.formatted_chars: List[str] = []

    def get_char_by_idx(self, idx: int) -> str:
        if idx < 0:
            return ""
        try:
            return self.original_name[idx]
        except IndexError:
            return ""

    def format(self) -> str:
        for idx, current_char in enumerate(self.original_name):
            self.format_current_char(current_char, idx)

        return "".join(self.formatted_chars)

    @abstractmethod
    def format_current_char(self, current_char: str, idx: int) -> None:
        pass
