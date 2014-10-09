"""
Save and load files in a semantic space format.
"""
import fs.zipfs
import scipy.io

try:
    import pandas as pd
except ImportError:
    print 'Warning: pandas not available. Importing to pandas will not work.'


class AbstractSemSpace(object):
    """Read and write from/to semantic space format."""
    def __init__(self, uri, mode='r'):
        self.root_file = self.create_fs(uri, mode)

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

    def write_from_pandas(self, df, readme=None):
        """Write a semantic space from pandas data frame"""
        if readme is not None:
            readme_title = readme['title']
            readme_desc = readme['description']
        rows = list(df.index)
        cols = list(df.columns)
        self.write_all(df.as_matrix(), rows, cols, readme_title, readme_desc)

    def close(self):
        self.root_file.close()

    def __del__(self):
        self.close()


class ZipSemSpace(AbstractSemSpace):
    """Read and write from/to semantic space format Zip file."""
    @staticmethod
    def create_fs(uri, mode):
        return fs.zipfs.ZipFS(uri, mode)