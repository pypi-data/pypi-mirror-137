# Grading Tools

[![build](https://github.com/worldquant-university/grading-tools/actions/workflows/build.yml/badge.svg)](https://github.com/worldquant-university/grading-tools/actions)
[![codecov](https://codecov.io/gh/worldquant-university/grading-tools/branch/main/graph/badge.svg?token=PV83R6T99N)](https://codecov.io/gh/worldquant-university/grading-tools)

This library allows you to compare student submissions to an answer, and provide
meaningful feedback. It currently accommodates basic Python data structures, `pandas`
Series and DataFrames, `scikit-learn` models, and images.

## Installation

```bash
$ pip install grading-tools
```

## Usage

```python
>>> from grading_tools.graders import PythonGrader
>>> sub = {"snake": "reptile", "frog": "reptile"}
>>> ans = {"snake": "reptile", "frog": "amphibian"}
>>> g = PythonGrader(sub, ans)
>>> g.grade_dict()
>>> g.return_feedback(html=False)
{
    'score': 0,
    'passed': False,
    'comment': "The value for the key `frog` doesn't match the expected result."
}
```

## License

`grading-tools` was created by
[Nicholas Cifuentes-Goodbody](https://github.com/ncgoodbody) at
[WorldQuant University](http://wqu.edu/). It is not currently licensed for reuse of
any kind.
