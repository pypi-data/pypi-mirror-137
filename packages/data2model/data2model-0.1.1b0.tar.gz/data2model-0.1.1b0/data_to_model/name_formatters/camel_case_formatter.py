from .name_formatter import NameFormatter


class CamelCaseFormatter(NameFormatter):
    """Convert from any to camel"""

    def format_current_char(self, current_char: str, idx: int) -> None:
        prev_char = self.get_char_by_idx(idx - 1)

        if current_char.isdigit() and idx == 0:
            self.formatted_chars.append(f"_{current_char}")
        elif not prev_char.isalnum():
            self.formatted_chars.append(current_char.upper())
        elif not current_char.isalnum():
            self.formatted_chars.append("")

        else:
            self.formatted_chars.append(current_char)
