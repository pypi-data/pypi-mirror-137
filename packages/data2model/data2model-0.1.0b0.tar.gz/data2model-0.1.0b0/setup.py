# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_to_model',
 'data_to_model.data_parsers',
 'data_to_model.generators',
 'data_to_model.models',
 'data_to_model.name_formatters',
 'data_to_model.type_detectors']

package_data = \
{'': ['*']}

install_requires = \
['aiocsv>=1.2.1,<2.0.0', 'aiofiles>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'data2model',
    'version': '0.1.0b0',
    'description': 'Python library and CLI tool for converting data to different Python data classes',
    'long_description': '# data2model\n\n![kdpv](https://github.com/dmitriiweb/data2model/raw/pre_production/imgs/matrix-g69866a888_640.jpg)\n\n![Tests](https://github.com/mCodingLLC/SlapThatLikeButton-TestingStarterProject/actions/workflows/tests.yml/badge.svg)\n\nPython library and CLI tool (in the nearest future) for generating different Python data classes from data.\n\nSupported data formats:\n- CSV\n\nSupported data classes:\n- [dataclasses](https://docs.python.org/3.8/library/dataclasses.html)\n\n## Requirements\n\n- Python 3.8+\n\n## Installation\n```shell\npip install data2model\n```\n\n## Usage\n```python\nimport asyncio\nimport pathlib\n\nfrom data_to_model import ModelGenerator\n\n\nfiles = [\n    {"input": pathlib.Path("example.csv"), "output": pathlib.Path("example.py")},\n]\n\n\nasync def model_generator(input_file: pathlib.Path, output_file: pathlib.Path):\n    mg = ModelGenerator(input_file)\n    model = await mg.get_model()\n    await model.save(output_file)\n\n\nasync def main():\n    tasks = [model_generator(i["input"], i["output"]) for i in files]\n    await asyncio.gather(*tasks)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n![output](https://github.com/dmitriiweb/data2model/raw/pre_production/imgs/carbon.png)\n',
    'author': 'Dmitrii Kurlov',
    'author_email': 'dmitriik@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmitriiweb/data2model',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
