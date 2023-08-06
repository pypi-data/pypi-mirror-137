"""Auxiliary functions to help with frequently performed tasks."""

from pathlib import Path
from typing import List, Optional, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import numpy as np
import pandas as pd

from . import compute
from .backends import backend
from .build import create_script
from .elements import Kicker, HKicker, VKicker, HMonitor, VMonitor, Segment
from .madx import run_script, run_orm


__all__ = ['compare_with_madx']


def compare_with_madx(lattice: Segment, *, orm: Literal[True, False] = False, madx: Optional[Union[str, Path]] = None):
    """Compute Twiss parameters for the given lattice and compare them to what MADX computes for the same lattice.

    .. note:: This function uses :meth:`Segment.apply_unique_labels` on the given lattice.

    Parameters
    ----------
    lattice : Segment
        The lattice for which the comparison is made.
    orm : bool
        Whether to compare the Orbit Response Matrix as well.
    madx : str or Path, optional
        File path to the MADX executable. This will be passed to the :mod:`dipas.madx.utils` functions.

    Returns
    -------
    global : pd.DataFrame
        Dataframe containing the following global lattice parameters:

            * Q1 (horizontal tune)
            * Q2 (vertical tune)

        Indices are ``['dipas', 'madx']`` and columns are the various lattice parameters.
    lattice : pd.DataFrame
        Dataframe containing the lattice functions as returned by :func:`dipas.compute.twiss`.
        The rows follow a MultiIndex where the first level contains the keys ``['dipas', 'madx']`` and the second level
        contains the elements labels along the lattice. The columns are the names of lattice functions (as returned by
        :func:`dipas.compute.twiss`, not the ones used by MADX).
    orm : pd.DataFrame
        Dataframe containing the Orbit Response Matrix as returned by :func:`dipas.madx.utils.run_orm` with an additional
        preceding index level along the rows. This additional index level contains the keys ``['dipas', 'madx']``.
    """
    result: List[pd.DataFrame] = []

    lattice.apply_unique_labels()
    script = create_script(beam=lattice[0].beam, sequence=lattice, errors=True)

    twiss = compute.twiss(lattice.makethin({Kicker: 2}, style={Kicker: 'edge'}))
    twiss['lattice'].index = twiss['lattice'].index.str.lower()
    twiss['lattice'] = twiss['lattice'].applymap(lambda x: x.item())  # Convert from tensor to float.

    twiss_madx, twiss_madx_meta = run_script(script, twiss=True, madx=madx)['twiss']
    twiss_madx['NAME'] = twiss_madx['NAME'].str.lower()
    twiss_madx.set_index('NAME', inplace=True)
    twiss_madx.columns = [_convert_twiss_col_name(c) for c in twiss_madx.columns]

    dipas_vs_madx = ['dipas', 'madx']
    global_params = ['Q1', 'Q2']
    result.append(pd.DataFrame(index=dipas_vs_madx, columns=global_params,
                               data=[[twiss[p].item() for p in global_params],
                                     [twiss_madx_meta[p] for p in global_params]]))

    labels = twiss['lattice'].index.intersection(twiss_madx.index)
    result.append(pd.concat((twiss['lattice'].loc[labels], twiss_madx.loc[labels]), join='inner', keys=dipas_vs_madx))

    if orm:
        kickers = lattice[HKicker] + lattice[VKicker]
        k_labels = [e.label for e in kickers]
        monitors = lattice[HMonitor] + lattice[VMonitor]
        m_labels = [e.label for e in monitors]

        orm_madx = run_orm(script, kickers=k_labels, monitors=m_labels, madx=madx)

        orm_x, orm_y = compute.orm(lattice, kickers=kickers, monitors=monitors, order=2)
        orm_xy = pd.DataFrame(index=orm_madx.index, columns=orm_madx.columns,
                              data=np.concatenate((backend.to_numpy(orm_x), backend.to_numpy(orm_y))))

        result.append(pd.concat((orm_xy, orm_madx), join='inner', keys=dipas_vs_madx))

    return tuple(result)


def _convert_twiss_col_name(col: str) -> str:
    if col in {'BETX', 'BETY', 'ALFX', 'ALFY', 'MUX', 'MUY'}:
        return f'{col[0]}{col[-1]}'.lower()
    return col.lower()
