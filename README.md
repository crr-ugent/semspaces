# Semantic spaces module

This is a python module for working with semantic spaces.

Currently supports a convenient input/output of the data from/to numpy and pandas.

## Installation

```bash
python setup.py install
```

## Usage

Writing a semantic space based on a numpy matrix:

```python
# simulate semantic space
import numpy as np

space = np.random.random((4,3))
rows = ['first', 'second', 'third', 'fourth']
columns = ['one', 'two', 'three']
readme_title = 'Random semantic space'
readme_description = 'This semantic space was genarated for demonstartion.\nHave fun!'

ssm = SemanticSpaceMarket('sspace.zip', 'w')
ssm.write_all(space, rows, columns, readme_title, readme_description)
ssm.close()
```

Write based on a pandas DataFrame:

```python
ssmp = SemanticSpaceMarket('sspace_pandas.zip', 'w')
ssmp.write_from_pandas(df, readme_title, readme_description)
ssmp.close()
```

Read a semantic space:

```python
rssm = SemanticSpaceMarket('sspace.zip', 'r')
rssm.read_all()
rssm.read_to_pandas()
rssm.close()
```
