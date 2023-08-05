import pathlib

from dataclasses import dataclass

import aiofiles


@dataclass()
class DataClassModel:
    content: str

    async def save(self, filepath: pathlib.Path) -> None:
        async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
            await f.write(self.content)
