from functools import partial
from importlib import resources
import os
import unittest
import warnings

import numpy as np

from dipas.aux import compare_with_madx
from dipas.build import from_file


class TestCompareWithMADX(unittest.TestCase):
    allclose = partial(np.allclose, atol=1e-6, rtol=1e-6)
    sequences = ['cryring', 'sis18']

    def test(self):
        for name in self.sequences:
            with self.subTest(sequence=name):
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    with resources.path('dipas.test.sequences', f'{name}.seq') as f_path:
                        lattice = from_file(str(f_path))
                df_global, df_twiss, df_orm = compare_with_madx(lattice, orm=True, madx=os.path.expanduser('~/bin/madx'))
                self.assertTrue(self.allclose(df_global.loc['dipas'], df_global.loc['madx']))
                self.assertTrue(self.allclose(df_twiss.loc['dipas'], df_twiss.loc['madx']))
                self.assertTrue(self.allclose(df_orm.loc['dipas'], df_orm.loc['madx']))


if __name__ == '__main__':
    unittest.main()
