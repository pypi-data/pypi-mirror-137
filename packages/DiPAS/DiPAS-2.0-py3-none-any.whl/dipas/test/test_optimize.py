import unittest

import numpy as np
from scipy.optimize import least_squares
from torch import tensor, float64

from dipas.backends import backend, PyTorch
from dipas.optimize import JacobianAdapter


@unittest.skipUnless(isinstance(backend, PyTorch), f'{JacobianAdapter.__name__} only works with {PyTorch.__name__} backend')
class TestJacobianAdapter(unittest.TestCase):
    def test(self):
        def f(x):
            return (x**2).sum()
        adapter = JacobianAdapter(f, ref_data=tensor([0., 0.], dtype=float64))
        result = least_squares(adapter, x0=np.array([1., 2.]), jac=adapter.jacobian, method='lm')
        self.assertAlmostEqual(result.x[0], 0, delta=1e-6)
        self.assertAlmostEqual(result.x[1], 0, delta=1e-6)


if __name__ == '__main__':
    unittest.main()
