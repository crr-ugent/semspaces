"""
Save and load files in a semantic space format.
"""
import codecs
import csv

import fs.zipfs
import scipy.io

try:
    import pandas as pd
except ImportError:
    print 'Warning: pandas not available. Importing to pandas will not work.'

try:
    import numpy as np
except ImportError:
    print 'Warning: pandas not available. Importing to numpy will not work.'


class AbstractSemanticSpace(object):
    """Read and write from/to semantic space format."""
    def __init__(self, fname, mode='r'):
        self.fname = fname
        self.mode = mode
        self.root_file = self.create_fs(fname, mode)

    @staticmethod
    def create_fs(uri, mode):
        """Create fs filesystem"""
        raise NotImplementedError(
            "create_fs(...) must be overriden by a subclass.")

    # Reading methods

    def read_rows(self):
        """Read rows."""
        if self.root_file.isfile('row-labels'):
            rows_file = self.root_file.open('row-labels', 'r')
            rows = [r.strip('\n') for r in rows_file.readlines()]
            rows_file.close()
            return rows
        else:
            return None

    def read_cols(self):
        """Read columns."""
        if self.root_file.isfile('col-labels'):
            cols_file = self.root_file.open('col-labels', 'r')
            cols = [c.strip('\n') for c in cols_file.readlines()]
            cols_file.close()
            return cols
        else:
            return None

    def read_readme(self):
        """Read columns."""
        if self.root_file.isfile('README.md'):
            readme_file = self.root_file.open('README.md', 'r')
            readme = readme_file.readlines()
            readme_file.close()
            if len(readme) >= 3:
                title = readme[0].strip()
                description = u''.join(readme[2:])
            elif len(readme) >= 1:
                title = readme[0].strip()
                description = u''
            else:
                print 'Warning: README.md exists but seems to be malformed.'
                return None
            return (title, description)
        else:
            return None

    def read_data(self):
        """Read matrix."""
        if self.root_file.isfile('data.mtx'):
            matrix_file = self.root_file.open('data.mtx', 'r')
            matrix = scipy.io.mmread(matrix_file)
            matrix_file.close()
            return matrix
        else:
            return None

    def read_all(self):
        """Convenience function for reading all data."""
        rows = self.read_rows()
        cols = self.read_cols()
        readme = self.read_readme()
        data = self.read_data()
        if readme is not None:
            return (data, rows, cols, readme[0], readme[1])
        else:
            return (data, rows, cols, None, None)

    def read_to_pandas(self):
        """Read to pandas dataframe"""
        data, rows, cols, r1, r2 = self.read_all()
        df = pd.DataFrame(data, index=rows)
        if cols is not None:
            df.columns = cols
        return df

    # Writing methods

    def write_rows(self, rows):
        """Write rows."""
        rows_file = self.root_file.open('row-labels', 'wb')
        for row in rows:
            rows_file.write('%s\n' % row)
        rows_file.close()

    def write_cols(self, cols):
        """Write columns."""
        cols_file = self.root_file.open('col-labels', 'wb')
        for col in cols:
            cols_file.write('%s\n' % col)
        cols_file.close()

    def write_readme(self, title, description=''):
        """Write README.md."""
        readme_file = self.root_file.open('README.md', 'wb')
        readme_file.write('%s\n\n%s' % (title, description))
        readme_file.close()

    def write_data(self, matrix, comment='', precision=None):
        """Write matrix."""
        matrix_file = self.root_file.open('data.mtx', 'wb')
        scipy.io.mmwrite(matrix_file, matrix, comment='comment',
                         precision=precision)
        matrix_file.close()

    def write_all(self, matrix, rows, cols=None, readme_title='',
                  readme_desc=''):
        """Convenience function for writing all elements at once."""
        self.write_data(matrix)
        self.write_rows(rows)
        if cols is not None:
            self.write_cols(cols)
        self.write_readme(readme_title, readme_desc)

    def write_from_pandas(self, df, readme_title='', readme_desc=''):
        """Write a semantic space from pandas data frame"""
        rows = list(df.index)
        cols = list(df.columns)
        self.write_all(df.as_matrix(), rows, cols, readme_title, readme_desc)

    def close(self):
        self.root_file.close()

    def __repr__(self):
        class_name = self.__class__.__name__
        return "%s('%s', '%s')" % (class_name, self.fname, self.mode)

    def __del__(self):
        self.close()


class ZipSemanticSpace(AbstractSemanticSpace):
    """Read and write from/to semantic space format Zip file."""
    @staticmethod
    def create_fs(uri, mode):
        return fs.zipfs.ZipFS(uri, mode)


class SemanticSpaceMarket(ZipSemanticSpace):
    """Default semantic space input output class"""


# Interoperability with  word2vec google tool

class W2VReader(object):
    """Reads word vectors in text format created by Google's word2vec tool"""
    @staticmethod
    def read_file(fname):
        """Return a tuple with (words, [list of vector values])."""
        fin = open(fname, 'rb')
        w2v_reader = csv.reader(fin, delimiter=' ')
        dims = w2v_reader.next()
        nrow, ncol = int(dims[0]), int(dims[1])
        word_vectors = []
        for row in w2v_reader:
            word = row[0]
            word_vector = [float(v) for v in row[1: ncol + 1]]
            word_vectors.append((word, word_vector))
        return word_vectors

    @classmethod
    def read_to_numpy(cls, fname):
        """Return a tuple with (words, numpy array with vectors)"""
        word_vectors = cls.read_file(fname)
        words, vectors = zip(*word_vectors)
        return(words, np.array(vectors))

    @classmethod
    def read_to_pandas(cls, fname):
        """Return a tuple with (words, numpy array with vectors)"""
        word_vectors = cls.read_file(fname)
        words, vectors = zip(*word_vectors)
        return pd.DataFrame(np.array(vectors), index=words)
