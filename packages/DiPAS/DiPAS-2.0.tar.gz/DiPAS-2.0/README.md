<div align="center">
  <a href="https://gitlab.com/Dominik1123/dipas">
    <img
        alt="dipas-logo"
        src="https://gitlab.com/Dominik1123/dipas/-/raw/develop/logo/logo.png"
        width="30%"
        style="display: block; margin-left: auto; margin-right: auto;"
    >
  </a>
</div>

[![pipeline](https://gitlab.com/Dominik1123/dipas/badges/develop/pipeline.svg)](https://gitlab.com/Dominik1123/dipas/-/commits/develop)
[![coverage](https://gitlab.com/Dominik1123/dipas/badges/develop/coverage.svg)](https://gitlab.com/Dominik1123/dipas/-/commits/develop)
[![pypi](https://img.shields.io/pypi/v/dipas.svg)](https://pypi.org/project/DiPAS/)
[![python](https://img.shields.io/pypi/pyversions/dipas.svg?style=flat-square)](https://pypi.org/project/dipas/)

-----

**DiPAS** is a program for differentiable simulations of particle accelerators. It acts as a framework and thus
supports a wide range of use cases such as [particle tracking](https://dipas.readthedocs.io/en/stable/usage/tracking.html)
or [optics calculations](https://dipas.readthedocs.io/en/stable/usage/optics.html) such as closed  orbit search or
computation of Twiss parameters.

The involved computations are backed by the [PyTorch](https://pytorch.org/) package which also provides the relevant
functionality for differentiation of user-defined quantities as well as a variety of gradient-based optimizers that integrate
with the thus derived quantities.

The DiPAS program can [parse MADX](https://dipas.readthedocs.io/en/stable/usage/building.html#Parsing-MADX-scripts)
lattice definitions and hence allows for zero-overhead importing of existing lattices.
In addition, it supports [custom lattice definitions](https://dipas.readthedocs.io/en/stable/usage/building.html#Using-the-build-API)
from provided element classes.

DiPAS can also be used via command line interface, see [`dipas --help`](https://dipas.readthedocs.io/en/stable/usage/cli.html)
for more information.


## Relevant links

* [Documentation](https://dipas.readthedocs.io/)
* [Examples](https://gitlab.com/Dominik1123/dipas/blob/master/examples)
* [PyPI Project](https://pypi.org/project/dipas/)


## Example usage

Minimizing loss along beamline by tuning quadrupoles:

```py
import numpy
from dipas.build import from_file
from dipas.elements import Quadrupole
import torch

lattice = from_file('example.madx')

for quad in lattice[Quadrupole]:
    quad.k1 = torch.nn.Parameter(quad.k1)

optimizer = torch.optim.Adam(lattice.parameters(), lr=1e-3)

particles = torch.from_numpy(numpy.load('particles.npy'))

while True:
    tracked, loss_val = lattice.linear(particles, recloss='sum')
    lost = 1 - tracked.shape[1] / particles.shape[1]
    if lost < 0.01:  # Fraction of particles lost less than 1%.
        break
    optimizer.zero_grad()
    loss_val.backward()
    optimizer.step()
```
