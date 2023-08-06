# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['area_unit_conversion']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['flake8-markdown = flake8_markdown:main']}

setup_kwargs = {
    'name': 'area-unit-conversion',
    'version': '1.0',
    'description': 'Module to convert unit of area from one system of units to another.',
    'long_description': '# **Area Unit Conversion** [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)]()\n\nPython module to convert unit of area from one system of units to another.\n\n## **Introduction** \n\nThis package was created for real estate business purposes. The availables units of length are the most commonly used in industry.\n\n**Availables units:**\n\n| Abbrev | Unit "EN"         | Unit "ES"            | value  |\n|:------:|:-----------------:|:--------------------:|:------:|\n| km²    | Square Kilometers | Kilómetros cuadrados | km2    |\n| m²     | Square Meters     | Metros cuadrados     | m2     |\n| mi²    | Square Miles      | Millas cuadradas     | mi2    |\n| yd²    | Square Yard       | Yardas cuadradas     | yd2    |\n| ft²    | Square Feet       | Pies cuadrados       | ft2    |\n| in²    | Square Inches     | Pulgadas cuadradas   | in2    |\n| ha     | Hectares          | Hectáreas            | ha     |\n| ac     | Acres             | Acres                | ac     |\n\n## **Installation**\n```\n$ pip install area_unit_conversion\n```\n\n## **Usage**\n\n### **convert**\n\nConverts unit of area from one system of units to another\n\n| Argument        | Type  | Default  | Description                       |\n|:---------------:|:-----:|:--------:|:---------------------------------:|\n| from_unit_type  | str   | None     | Original system of unit area      |\n| to_unit_type    | str   | None     | Desired system of unit area       |\n| value           | float | 0        | Area value to convert             |\n\n\n```\nimport area_unit_conversion\n\narea_unit_conversion.convert(\'m2\',\'ha\',10000) \n\n# Return 1\n\n```\n\n### **get_units_of_length**\n\nLists available units of length\n\n| Argument | Type  | Default  | Description          |\n|:--------:|:-----:|:--------:|:--------------------:|\n| lang     | str   | "en"     | iso code of language |\n\n Options: "es" | "en"\n\n```\nimport area_unit_conversion\n\narea_unit_conversion.get_units_of_length() \n\n# Return\n[\n    {\n        \'abbreviation\': \'km²\', \n        \'value\': \'km2\', \n        \'name\': \'Square Kilometers\'\n    },{   \n        \'abbreviation\': \'m²\', \n        \'value\': \'m2\', \n        \'name\': \'Square Meters\'\n    },{\n        \'abbreviation\': \'mi²\',\n        \'value\': \'mi2\',\n        \'name\': \'Square Miles\'\n    }, \n    \n    etc. , etc.\n    }\n]\n\n```\n\n## **Test**\nRunning tests:\n```\n$ pytest\n```\n\nChecking the package installs correctly with different Python versions and interpreters.\n\nTested with python3.6, python3.7, python3.8, python3.9 and python3.10 versions:\n```\n$ tox\n```\n\n## **Contributing**\nContributions are welcome - submit an issue/pull request.',
    'author': 'Rafael Suarez',
    'author_email': 'rafael.asg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rafaelsuarezg/area_unit_conversion',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
