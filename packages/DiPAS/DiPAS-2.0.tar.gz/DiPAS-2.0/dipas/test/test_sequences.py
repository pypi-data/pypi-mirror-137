import glob
import os.path
from pathlib import Path
import unittest
import warnings

from dipas.backends import backend, PyTorch, Numpy
from dipas.build import from_file

f_names = {Path(f).stem: f for f in glob.glob(os.path.join('sequences', '*.seq'))}


class TestHADES(unittest.TestCase):
    def test(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            lattice = from_file(f_names['hades'])
        self.assertEqual(len(list(lattice.children())), len(lattice.elements))
        if isinstance(backend, PyTorch):
            self.assertEqual(len(list(lattice.parameters())), 21)
        elif isinstance(backend, Numpy):
            self.assertEqual(len(list(lattice.parameters())), 0)
        else:
            warnings.warn(f'No parameter count reference value for backend {backend!r}')


class TestCRYRING(unittest.TestCase):
    def test(self):
        lattice = from_file(f_names['cryring'])
        self.assertEqual(len(lattice.elements), 182)
        self.assertEqual(len(list(lattice.children())), len(lattice.elements))


class TestSIS18(unittest.TestCase):
    def test(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            lattice = from_file(f_names['sis18'])
        self.assertEqual(len(list(lattice.children())), len(lattice.elements))


if __name__ == '__main__':
    unittest.main()
