# data2model

![kdpv](https://github.com/dmitriiweb/data2model/raw/pre_production/imgs/matrix-g69866a888_640.jpg)

![Tests](https://github.com/mCodingLLC/SlapThatLikeButton-TestingStarterProject/actions/workflows/tests.yml/badge.svg)

Python library and CLI tool (in the nearest future) for generating different Python data classes from data.

Supported data formats:
- CSV

Supported data classes:
- [dataclasses](https://docs.python.org/3.8/library/dataclasses.html)

## Requirements

- Python 3.8+

## Installation
```shell
pip install data2model
```

## Usage
```python
import asyncio
import pathlib

from data_to_model import ModelGenerator


files = [
    {"input": pathlib.Path("example.csv"), "output": pathlib.Path("example.py")},
]


async def model_generator(input_file: pathlib.Path, output_file: pathlib.Path):
    mg = ModelGenerator(input_file)
    model = await mg.get_model()
    await model.save(output_file)


async def main():
    tasks = [model_generator(i["input"], i["output"]) for i in files]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
```
![output](https://github.com/dmitriiweb/data2model/raw/pre_production/imgs/carbon.png)
