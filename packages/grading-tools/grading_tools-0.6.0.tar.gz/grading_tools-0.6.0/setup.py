# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grading_tools']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.6,<4.0.0',
 'Pillow>=9.0.1,<10.0.0',
 'category-encoders>=2.3.0,<3.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.1,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'statsmodels>=0.13.1,<0.14.0',
 'wqet-grader>=0.1.18,<0.2.0']

setup_kwargs = {
    'name': 'grading-tools',
    'version': '0.6.0',
    'description': 'Tools for evaluating student submissions.',
    'long_description': '# Grading Tools\n\n[![build](https://github.com/worldquant-university/grading-tools/actions/workflows/build.yml/badge.svg)](https://github.com/worldquant-university/grading-tools/actions)\n[![codecov](https://codecov.io/gh/worldquant-university/grading-tools/branch/main/graph/badge.svg?token=PV83R6T99N)](https://codecov.io/gh/worldquant-university/grading-tools)\n\nThis library allows you to compare student submissions to an answer, and provide\nmeaningful feedback. It currently accommodates basic Python data structures, `pandas`\nSeries and DataFrames, `scikit-learn` models, and images.\n\n## Installation\n\n```bash\n$ pip install grading-tools\n```\n\n## Usage\n\n```python\n>>> from grading_tools.graders import PythonGrader\n>>> sub = {"snake": "reptile", "frog": "reptile"}\n>>> ans = {"snake": "reptile", "frog": "amphibian"}\n>>> g = PythonGrader(sub, ans)\n>>> g.grade_dict()\n>>> g.return_feedback(html=False)\n{\n    \'score\': 0,\n    \'passed\': False,\n    \'comment\': "The value for the key `frog` doesn\'t match the expected result."\n}\n```\n\n## License\n\n`grading-tools` was created by\n[Nicholas Cifuentes-Goodbody](https://github.com/ncgoodbody) at\n[WorldQuant University](http://wqu.edu/). It is not currently licensed for reuse of\nany kind.\n',
    'author': 'Nicholas Cifuentes-Goodbody',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
