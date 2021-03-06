# Semantic spaces module

This is a python module for working with semantic spaces.

Currently supports a convenient input/output of the data from/to numpy and pandas.

## Installation

```bash
python setup.py install
```

## Usage

### Semantic space market input output

Writing a semantic space based on a numpy matrix:

```python
# simulate semantic space
import numpy as np

space = np.random.random((4,3))
rows = ['first', 'second', 'third', 'fourth']
columns = ['one', 'two', 'three']
readme_title = 'Random semantic space'
readme_description = 'This semantic space was genarated for demonstration.\nHave fun!'


# save semantic space
from semspaces.io import SemanticSpaceMarket

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

### Reading Google's word2vec output

To read csv file produced by Google's word2vec tool:

```python
from semspaces.io import W2VReader

word_vectors = W2VReader.read_file('word2vec-vectors.csv')
words, space = W2VReader.read_to_numpy('word2vec-vectors.csv')
words_space = W2VReader.read_to_pandas('word2vec-vectors.csv')
```
