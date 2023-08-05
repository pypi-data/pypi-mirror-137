from .name_formatter import NameFormatter


class SnakeCaseFormatter(NameFormatter):
    """Convert from any to snake"""

    def format_current_char(self, current_char: str, idx: int) -> None:
        if not current_char.isalpha() and not current_char.isdigit():
            self.formatted_chars.append("_")

        elif current_char.isdigit() and idx == 0:
            self.formatted_chars.append(f"_{current_char}")

        elif current_char.isupper():
            self.formatted_chars.append(self._format_upper(current_char, idx))

        else:
            self.formatted_chars.append(current_char)

    def _format_upper(self, upper: str, idx: int) -> str:
        prev_char = self.get_char_by_idx(idx - 1)
        next_char = self.get_char_by_idx(idx + 1)

        if idx == 0 or idx == len(self.original_name) - 1:
            return upper.lower()

        if prev_char.isupper() and not next_char.isupper():
            return f"{upper.lower()}_"

        if not prev_char.isupper():
            return f"_{upper.lower()}"

        return upper.lower()
