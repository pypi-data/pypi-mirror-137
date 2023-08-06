# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dh2vrml']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.3,<9.0.0',
 'numpy>=1.21,<2.0',
 'pandas>=1.3,<2.0',
 'x3d>=4.0.47,<5.0.0',
 'xmlschema>=1.9.2,<2.0.0']

entry_points = \
{'console_scripts': ['dh2vrml = dh2vrml.cli:main']}

setup_kwargs = {
    'name': 'dh2vrml',
    'version': '0.1.6',
    'description': 'Library and CLI tool to convert Denavit–Hartenberg parameters to an X3D model',
    'long_description': '# dh2vrml\n\ndh2vrml is a utility for converting Denavit–Hartenberg parameters into X3D models, with a particular focus on creating outputs suitable for use as a MATLAB Simulink VR Sink.\n\n## Installation\n\n```\npip install dh2vrml\n```\n\n## Usage\n\n```\ndh2vrml -f <file_name>\n```\n\n### Parameters\n\n- `type`: Joint type, either `revolute` or `prismatic`\n    - This refers to the joint at index `i - 1`, (i.e. the first joint is the base joint)\n- `d`, `theta`, `r`, `alpha`: DH parameters as specified on [Wikipedia](https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters)\n- `color`: Color of the joint and link at index `i`, in RGB format\n    - Values are floats ranging from 0 to 1\n    - The end effector is always colored `(0, 1, 1)`, (cyan)\n- `scale`: The relative size of joints and links\n    - Links are scaled cross sectionally (position is not affected)\n    - Joints are scaled volumetrically\n    - The first value scales both the base joint and the joint after it\n    - If no value is provided, the last provided value is used\n        - Scale of the model can be set globally by only providing `scale` for the first set of parameters\n\n### Supported file types\n\n#### YAML\n\n```yaml\n- type: revolute  \n  d: 1.5\n  theta: 0\n  r: 3\n  alpha: 0\n  color: [1, 0, 0]\n\n- type: revolute\n  d: 2\n  theta: 0\n  r: 4\n  alpha: 3.14159265359\n  color: [0, 0, 1]\n\n- type: prismatic\n  d: 3\n  theta: 0\n  r: 0\n  alpha: 0\n  color: [1, 0, 1]\n```\n\n#### CSV\n\n```csv\nd ,theta ,r ,alpha        ,type     , color\n2 ,0     ,0 ,1.5707963268 ,revolute , 1 0 0\n0 ,0     ,2 ,0            ,revolute , 0 1 0\n```\n\n#### Python\n\nFor the sake of making calculations involving `pi` easier, Python files are supported.\n\n> Beware: dh2vrml will blindly import and run whatever code is provided, always inspect the contents of the file before importing\n\n```py\nfrom math import pi\n\nparams = [\n    {\n        "type": "revolute",\n        "d": 2,\n        "theta": pi/2,\n        "r": 0,\n        "alpha": pi/2\n    },\n    {\n        "type": "revolute",\n        "d": 2,\n        "theta": pi/2,\n        "r": 0,\n        "alpha": -pi/2\n    },\n    {\n        "type": "revolute",\n        "d": 2,\n        "theta": pi/2,\n        "r": 2,\n        "alpha": 0\n    },\n]\n```\n',
    'author': 'Jasper Chan',
    'author_email': 'jasperchan515@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gigahawk/dh2vrml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
