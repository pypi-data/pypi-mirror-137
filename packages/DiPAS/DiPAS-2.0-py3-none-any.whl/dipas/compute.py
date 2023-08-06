"""Convenience functions for computing various simulation related quantities."""

from dataclasses import dataclass, field, InitVar
from functools import reduce
import itertools as it
import math
import operator as op
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple, Union
from typing_extensions import Literal

import pandas as pd

from .backends import backend
from .elements import AlignmentError  # Import this so that `get_type_hints` works on functions of this module.
from .elements import BPMError
from .elements import Kicker, Monitor, MultiElementSelector, SingleElementSelector, Segment, Utilities, TransferMap
from .elements import Number


__all__ = ['closed_orbit', 'linear_closed_orbit', 'twiss', 'orm', 'transfer_maps', 'InitialLatticeParameters']

TensorType = backend.TensorType

ORBIT_DIVERGENCE_THRESHOLD = 1e3

Fs = backend.functions
La = backend.linalg
I2 = backend.make_id_matrix(2)
I4 = backend.make_id_matrix(4)


class InputError(Exception):
    pass


class ConvergenceError(Exception):
    pass


class DivergingOrbitError(ConvergenceError):
    pass


class UnstableLatticeError(Exception):
    pass


@dataclass
class InitialLatticeParameters:
    beta_x: Number
    beta_y: Number
    orbit: TensorType = field(default_factory=lambda: backend.make_zeros(6, 1))
    x: InitVar[Number] = None
    px: InitVar[Number] = None
    y: InitVar[Number] = None
    py: InitVar[Number] = None
    t: InitVar[Number] = None
    pt: InitVar[Number] = None
    alpha_x: Number = 0.
    alpha_y: Number = 0.
    mu_x: Number = 0.
    mu_y: Number = 0.
    dispersion: TensorType = field(default_factory=lambda: backend.make_zeros(6, 1))
    dx: InitVar[Number] = None
    dpx: InitVar[Number] = None
    dy: InitVar[Number] = None
    dpy: InitVar[Number] = None

    def __post_init__(self, x: Number, px: Number, y: Number, py: Number, t: Number, pt: Number,
                      dx: Number, dpx: Number, dy: Number, dpy: Number):
        if len(self.orbit.shape) == 1:
            self.orbit = self.orbit.reshape(-1, 1)
        if len(self.dispersion.shape) == 1:
            self.dispersion = self.dispersion.reshape(-1, 1)
        if self.dispersion.shape[0] == 4:
            _dispersion = backend.make_zeros(6, 1)
            _dispersion[:4] = self.dispersion
            self.dispersion = _dispersion

        if x is not None:
            self.orbit[0, 0] = x
        if px is not None:
            self.orbit[1, 0] = px
        if y is not None:
            self.orbit[2, 0] = y
        if py is not None:
            self.orbit[3, 0] = py
        if t is not None:
            self.orbit[4, 0] = t
        if pt is not None:
            self.orbit[5, 0] = pt

        if dx is not None:
            self.dispersion[0, 0] = dx
        if dpx is not None:
            self.dispersion[1, 0] = dpx
        if dy is not None:
            self.dispersion[2, 0] = dy
        if dpy is not None:
            self.dispersion[3, 0] = dpy
        self.dispersion[5, 0] = 1.0

        for name in map('_'.join, it.product(('beta', 'alpha', 'mu'), 'xy')):
            value = getattr(self, name)
            if isinstance(value, (int, float)):
                setattr(self, name, backend.from_numbers(value))


@dataclass
class TwissData:
    """Twiss parameters, dispersion and orbit data.

    The following attributes are available:

    * orbit: (6, 1)-shaped tensor containing the six-dimensional orbit (x, px, y, py, t, pt)
    * x, px, y, py, t, pt: individual components of the `orbit`
    * bx, by: horizontal and vertical beta function
    * ax, ay: horizontal and vertical derivative of the beta function (alpha = -0.5*dbeta/ds)
    * mx, my: horizontal and vertical phase advance in units of [2*pi]
    * dispersion: (4, 1)-shaped tensor containing the four-dimensional dispersion (dx, dpx, dy, dpy)
    * dx, dpx, dy, dpy: individual components of the `dispersion`
    """

    orbit: TensorType
    bx: Number
    by: Number
    ax: Number
    ay: Number
    mx: Number
    my: Number
    dispersion: TensorType

    def __post_init__(self):
        if len(self.orbit.shape) == 1:
            self.orbit = self.orbit.reshape(-1, 1)
        if len(self.dispersion.shape) == 1:
            self.dispersion = self.dispersion.reshape(-1, 1)
        self.dispersion = self.dispersion[:4]

    @property
    def x(self):
        return self.orbit[0, 0]

    @property
    def px(self):
        return self.orbit[1, 0]

    @property
    def y(self):
        return self.orbit[2, 0]

    @property
    def py(self):
        return self.orbit[3, 0]

    @property
    def t(self):
        return self.orbit[4, 0]

    @property
    def pt(self):
        return self.orbit[5, 0]

    @property
    def dx(self):
        return self.dispersion[0, 0]

    @property
    def dpx(self):
        return self.dispersion[1, 0]

    @property
    def dy(self):
        return self.dispersion[2, 0]

    @property
    def dpy(self):
        return self.dispersion[3, 0]


def twiss(lattice: Segment,
          *,
          order: Literal[1, 2] = 2,
          co_args: Optional[Dict] = None,
          initial: Optional[InitialLatticeParameters] = None
          ) -> Dict:
    """Compute various lattice functions and parameters.

    .. note:: :class:`Kicker`s must be sliced via :meth:`~Kicker.makethin` beforehand in order for ``twiss`` to work.

    Parameters
    ----------
    lattice : :class:`Segment`
    order : int
        Order of truncation for the transfer maps of lattice elements.
    co_args : dict
        Keyword arguments for :func:`closed_orbit`.
    initial : :class:`InitialLatticeParameters`
        Initial lattice parameters to be used instead of the values from the periodic solution. If this argument is
        provided the periodic solution won't be computed; all values are taken from the `initial` specification.

    Returns
    -------
    twiss : dict
        Contains the following key-value pairs:
           * "Q1" -- first mode tune
           * "Q2" -- second mode tune
           * "coupling_matrix" -- the 2x2 coupling matrix
           * "lattice" -- a data frame with element labels as indices and the following columns:
              * "x", "y", "px", "py" -- the values of the closed orbit.
              * "bx", "ax", "mx", "by", "ay", "my", "dx", "dpx", "dy", "dpy" -- linear lattice functions beta and alpha
                as well as phase advance and dispersion for the two modes; the phase advance is given in units of [2*pi].

    Raises
    ------
    :class:`UnstableLatticeError` -- in case either mode is unstable.
    """
    if len(set(e.label for e in lattice.elements)) < len(lattice):
        raise InputError('Lattice elements must have unique labels (use lattice.apply_unique_labels() beforehand)')
    if initial is None:
        if co_args is None:
            co_args = {}
        co_args.setdefault('order', order)
        co, R = closed_orbit(lattice, **co_args, return_transfer_matrix=True)
        R = Utilities.symplectify(R)
        dispersion = backend.zeros_like(co)
        dispersion[5, 0] = 1
        dispersion[:4] = La.solve(I4 - R[:4, :4], R[:4, -1:])
        A, B = R[0:2, 0:2], R[0:2, 2:4]
        C, D = R[2:4, 0:2], R[2:4, 2:4]
        CB = C - Utilities.S2 @ backend.transpose(B) @ Utilities.S2
        det = La.det(CB)
        trace = La.trace(A - D) / 2
        coupling = det + trace**2
        if coupling < 0:
            raise UnstableLatticeError('Unstable due to coupling')
        elif coupling == 0:
            coupling_matrix = I2
        else:
            coupling_matrix = -CB / (trace + math.copysign(Fs.sqrt(coupling), trace))
        beta_x, alpha_x = _compute_initial_beta_alpha(A - B @ coupling_matrix, mode=1)
        beta_y, alpha_y = _compute_initial_beta_alpha(D + coupling_matrix @ B, mode=2)
        mu_x, mu_y = backend.from_numbers(0.), backend.from_numbers(0.)
    else:
        R = None
        coupling_matrix = backend.make_zeros(2, 2)
        co = initial.orbit
        beta_x = initial.beta_x
        beta_y = initial.beta_y
        alpha_x = initial.alpha_x
        alpha_y = initial.alpha_y
        mu_x = initial.mu_x
        mu_y = initial.mu_y
        dispersion = initial.dispersion
    labeled_transfer_matrices = lattice.transfer_maps('local', order=order, labels=True, unfold_alignment_errors=True, indices=1, d0=co)
    labels, transfer_matrices = zip(*labeled_transfer_matrices)
    transfer_matrices = [(None, None, coupling_matrix), *transfer_matrices]  # First item is the initial value for the following 'accumulate'.
    decoupled_matrices = it.accumulate(transfer_matrices, lambda x, y: _decouple_transfer_matrix(y, x[-1]))
    decoupled_matrices = (x[:2] for x in it.islice(decoupled_matrices, 1, None))  # Drop auxiliary item with initial coupling matrix.
    M1, M2 = zip(*decoupled_matrices)
    beta_alpha_mu_x = it.accumulate([(beta_x, alpha_x, mu_x), *M1], lambda x, y: _track_beta_alpha_mu(y, *x))
    beta_alpha_mu_y = it.accumulate([(beta_y, alpha_y, mu_y), *M2], lambda x, y: _track_beta_alpha_mu(y, *x))
    dispersion = it.accumulate([dispersion, *transfer_matrices[1:]], lambda x, y: _track_dispersion(y, x))
    dispersion = (x[:4].squeeze() for x in dispersion)
    lattice_functions = [beta_alpha_mu_x, beta_alpha_mu_y, dispersion]
    labels = ('#s',) + labels  # Add start label, corresponding to initial twiss values.
    exit_indices = {tuple(g)[-1][0] for k, g in it.groupby(enumerate(labels), key=op.itemgetter(1))}
    for i, lat_func in enumerate(lattice_functions):
        lattice_functions[i] = it.compress(lat_func, (i in exit_indices for i in it.count()))
    co = it.chain([co], lattice.transfer_maps('accumulate', order=order, indices=0, d0=co))
    co = (x[:4].squeeze() for x in co)
    data = {'lattice': pd.DataFrame(
        data=[list(it.chain.from_iterable(row)) for row in zip(co, *lattice_functions)],
        index=list(it.compress(labels, (i in exit_indices for i in it.count()))),
        columns=['x', 'px', 'y', 'py', 'bx', 'ax', 'mx', 'by', 'ay', 'my', 'dx', 'dpx', 'dy', 'dpy'],
        dtype=object
    )}
    data.update(coupling_matrix=coupling_matrix)
    data.update(Q1=data['lattice'].iloc[-1]['mx'], Q2=data['lattice'].iloc[-1]['my'])
    data.update(one_turn_matrix=R)
    return data


def twiss_target(lattice: Segment,
                 initial: InitialLatticeParameters,
                 *,
                 order: Literal[1, 2] = 2,
                 ) -> Tuple[TwissData, TensorType]:
    """Compute the orbit and various lattice functions at the end of a beamline (target).

    .. note::
       :class:`Kicker`s must be sliced via :meth:`~Kicker.makethin` beforehand in order for ``twiss_target`` to work.

    Parameters
    ----------
    lattice : :class:`Segment`
        The lattice of the beamline.
    initial : :class:`InitialLatticeParameters`
        Initial lattice parameters at the beginning of the beamline.
    order : int
        Order of truncation for the transfer maps of lattice elements.

    Returns
    -------
    twiss : :class:`TwissData`
        Containing Twiss parameters, dispersion and orbit data at the end of the beamline.
    coupling_matrix : Tensor, shape (2,2)
        The coupling matrix at the end of the beamline.
    """
    co = initial.orbit
    beta_x = initial.beta_x
    beta_y = initial.beta_y
    alpha_x = initial.alpha_x
    alpha_y = initial.alpha_y
    mu_x = initial.mu_x
    mu_y = initial.mu_y
    dispersion = initial.dispersion

    transfer_matrices = lattice.transfer_maps('local', order=order, unfold_alignment_errors=True, indices=1, d0=co)

    transfer_matrices = [(None, None, backend.make_zeros(2, 2)), *transfer_matrices]  # First item is the initial value for the following 'accumulate'.
    decoupled_matrices = it.accumulate(transfer_matrices, lambda x, y: _decouple_transfer_matrix(y, x[-1]))
    decoupled_matrices = it.islice(decoupled_matrices, 1, None)  # Drop auxiliary item with initial coupling matrix.

    M1, M2, coupling_matrices = zip(*decoupled_matrices)
    bx, ax, mx = reduce(lambda x, y: _track_beta_alpha_mu(y, *x), M1, (beta_x, alpha_x, mu_x))
    by, ay, my = reduce(lambda x, y: _track_beta_alpha_mu(y, *x), M2, (beta_y, alpha_y, mu_y))
    dispersion = reduce(lambda x, y: _track_dispersion(y, x), transfer_matrices[1:], dispersion)[:4].squeeze()
    co = lattice.transfer_maps('reduce', order=order, indices=0, d0=co)

    return TwissData(orbit=co, bx=bx, ax=ax, mx=mx, by=by, ay=ay, my=my, dispersion=dispersion), coupling_matrices[-1]


def _decouple_transfer_matrix(M: TensorType, coupling_matrix: TensorType) -> Tuple[TensorType, TensorType, TensorType]:
    """Decouple the given transfer matrix into two independent modes.

    Parameters
    ----------
    M : Tensor, shape (m, n) where m, n >= 4
        Transfer matrix representing the transverse dimensions (+ optionally longitudinal dimension which is ignored).
    coupling_matrix : Tensor, shape (2, 2)
        The accumulated coupling matrix along the lattice.

    Returns
    -------
    M1 : Tensor, shape (2, 2)
        Upper-left block of decoupled transfer matrix (corresponding to mode 1).
    M2 : Tensor, shape(2, 2)
        Lower-right block of decoupled transfer matrix (corresponding to mode 2).
    coupling_matrix_updated : Tensor, shape (2, 2)
        The accumulated, updated coupling matrix, including the effect from the decoupled transfer matrix `M`.
    """
    S2 = Utilities.S2
    A, B = M[0:2, 0:2], M[0:2, 2:4]
    C, D = M[2:4, 0:2], M[2:4, 2:4]
    if Fs.all(B == 0) and Fs.all(C == 0):
        E, F = A, D
        coupling_matrix = -F @ coupling_matrix @ S2 @ backend.transpose(E) @ S2 / La.det(E)
    else:
        E = A - B @ coupling_matrix
        F = D - C @ S2 @ backend.transpose(coupling_matrix) @ S2
        coupling_matrix = (C - D @ coupling_matrix) @ S2 @ backend.transpose(E) @ S2 / La.det(E)
    return E, F, coupling_matrix


def _compute_initial_beta_alpha(M: TensorType, mode: Literal[1, 2]) -> Tuple[TensorType, TensorType]:
    """Compute the initial beta and alpha values for the given mode and corresponding transfer matrix.

    Parameters
    ----------
    M : Tensor, shape (2, 2)
        Diagonal block of decoupled transfer matrix.
    mode : int
        Indicates the mode (only used for error message).

    Raises
    ------
    :class:`UnstableLatticeError` -- in case the given mode is unstable.
    """
    trace = La.trace(M) / 2
    if Fs.abs(trace) >= 1:
        raise UnstableLatticeError(f'Mode {mode} is unstable')
    sin_mu = math.copysign(Fs.sqrt(- M[0, 1] * M[1, 0] - 0.25 * (M[0, 0] - M[1, 1])**2),
                           M[0, 1])
    return M[0, 1] / sin_mu, (M[0, 0] - M[1, 1]) / (2 * sin_mu)


def _track_beta_alpha_mu(M: TensorType, beta: TensorType, alpha: TensorType, mu: TensorType) -> Tuple[TensorType, TensorType, TensorType]:
    """Track beta and alpha values corresponding to one (decoupled) mode through an element represented by the
       transfer matrix `M`.

    Parameters
    ----------
    M : Tensor, shape (2, 2)
        Diagonal block of decoupled transfer matrix.
    beta : Tensor, shape []
        Initial beta value.
    alpha : Tensor, shape []
        Initial alpha value.
    mu : Tensor, shape []
        Initial phase advance.

    Returns
    -------
    beta : Tensor, shape []
        Beta value after being tracked through `M`.
    alpha : Tensor, shape []
        Alpha value after being tracked through `M`.
    mu : Tensor, shape []
        Phase advance after being tracked through `M` in units of [2*pi].
    """
    det_M = La.det(M)
    t = M @ backend.stack((beta, -alpha))
    return ((t[0]**2 + M[0, 1]**2) / det_M / beta,
            -(t[0]*t[1] + M[0, 1]*M[1, 1]) / det_M / beta,
            mu + Fs.arctan2(M[0, 1], t[0]) / (2*math.pi))


def _track_dispersion(R: TensorType, dispersion: TensorType) -> TensorType:
    """Track the dispersion vector through an element represented by the transfer matrix R.

    Parameters
    ----------
    R : Tensor, shape (6, 6)
        Transfer matrix of the element.
    dispersion : Tensor, shape (6, 1)
        Dispersion at the entrance of the element.

    Returns
    -------
    dispersion : Tensor, shape (6, 1)
        Dispersion at the exit of the element.
    """
    new = R @ dispersion
    new[4, 0] = 0.
    new[5, 0] = 1.0
    return new


class ORMData(NamedTuple):
    x: TensorType
    y: TensorType


def orm(lattice: Segment, *,
        kickers: Union[MultiElementSelector, Sequence[Union[SingleElementSelector, Kicker]]],
        monitors: Union[MultiElementSelector, Sequence[Union[SingleElementSelector, Monitor, BPMError]]],
        kicks: Tuple[float, float] = (-0.001, 0.001),
        order: Literal[1, 2] = 2,
        co_args: Optional[dict] = None) -> ORMData:
    """Compute the orbit response matrix (ORM) for the given lattice, kickers and monitors.

    Parameters
    ----------
    lattice : Segment
    kickers : MultiElementSelector or list of SingleElementSelector
        Can be an identifier for selecting multiple kickers, or a list of identifiers each selecting a single kicker
        or a list of :class:`Kicker` elements directly.
    monitors : MultiElementSelector or list of SingleElementSelector
        Can be an identifier for selecting multiple monitors, or a list of identifiers each selecting a single monitor
        or a list of :class:`Monitor` elements directly.
    kicks : 2-tuple of float
        The kick strengths to be used for measuring the orbit response.
    order : int
        See :func:`closed_orbit`.
    co_args : dict
        Additional arguments for the closed orbit search.

    Returns
    -------
    orm_x, orm_y : Tensor
        Shape `len(monitors), len(kickers)`.
    """
    co_args = co_args or {}
    if isinstance(kickers, (tuple, list)):
        kickers = [k if isinstance(getattr(k, 'element', None), Kicker) else lattice[k] for k in kickers]
    else:
        kickers = lattice[kickers]
    if isinstance(monitors, (tuple, list)):
        monitors = [m if isinstance(getattr(m, 'element', None), Monitor) else lattice[m] for m in monitors]
    else:
        monitors = lattice[monitors]
    m_indices = list(map(lattice.get_element_index, monitors))
    orm_x = backend.make_zeros(len(monitors), len(kickers))
    orm_y = backend.make_zeros(len(monitors), len(kickers))
    for ik, kicker in enumerate(kickers):
        co_values = []
        for kick in kicks:
            kicker.kick += kick
            thin = lattice.makethin({Kicker: 2}, style={Kicker: 'edge'})  # These are the settings used by MADX.
            co = thin.transfer_maps('accumulate', order=order, indices=0, d0=closed_orbit(thin, order=order, **co_args))
            co_values.append([m.readout(co[i]) for i, m in zip(m_indices, monitors)])
            kicker.kick -= kick
        for im in range(len(monitors)):
            orm_x[im, ik] += (co_values[1][im] - co_values[0][im])[0, 0] / (kicks[1] - kicks[0])
            orm_y[im, ik] += (co_values[1][im] - co_values[0][im])[1, 0] / (kicks[1] - kicks[0])
    return ORMData(orm_x, orm_y)


def closed_orbit(lattice: Segment, *,
                 order: Literal[1, 2] = 2,
                 max_iter: Optional[int] = None,
                 tolerance: float = 1e-6,
                 initial_guess: Optional[TensorType] = None,
                 return_transfer_matrix: bool = False) -> Union[TensorType, Tuple[TensorType, TensorType]]:
    r"""Closed orbit search for a given order on the given lattice.

    The given lattice may contain `Element`s as well as `AlignmentError`s. Alignment errors are treated as additional
    elements that wrap the actual element: entrance transformations coming before the element, in order, and exit
    transformations being placed after, in reverse order. The closed orbit search is a first-order iterative procedure
    with where each update :math:`x_{\Delta}` is computed as the solution of the following set of linear equations::

    .. math:: \left[\mathbb{1} - R\right]\, x_{\Delta} = x_1 - x_0

    where :math:`R` is the one-turn transfer matrix and :math:`x_1` is the orbit after one turn when starting from
    :math:`x_0`. :math:`R` represents the Jacobian of the orbit w.r.t. itself.

    Parameters
    ----------
    lattice : Segment
    order : int
        Transfer maps used for tracking the closed orbit guess are truncated at the specified order (however the linear
        response `R` does contain second feed-down terms from `T`, if any).
    max_iter : int, optional
        Maximum number of iterations.
    tolerance : float, optional
        Maximum L1 distance between initial orbit and tracked orbit after one turn for convergence.
    initial_guess : Tensor
        Initial guess for the closed orbit search; must be of shape (6,1).
    return_transfer_matrix : bool, default = False
        If `True` then the one-turn transfer matrix is returned along the computed closed orbit as a tuple: ``x, R``.
        Note that during the closed orbit search, after the deviation reached below the specified `threshold`, one
        additional update to the closed orbit `x` is performed but not to the transfer matrix `R`. For that reason the
        matrix `R` might deviate slightly from the matrix obtained by :func:`elements.process_transfer_maps` when using
        the returned orbit `x`.

    Returns
    -------
    closed_orbit : Tensor
        Tensor of shape (6,) containing the closed orbit in the transverse coordinates and zeros for the longitudinal
        coordinates.
    one_turn_transfer_matrix : Tensor, optional
        Tensor of shape (6, 6) representing the one-turn transfer matrix. This is only returned if the argument for
        `return_transfer_matrix` is set to `True`.

    Raises
    ------
    ConvergenceError
        If the closed orbit search did not converge within the specified number of iterations for the given tolerance.
    DivergingOrbitError
        If a component of the closed orbit estimate exceeds the :data:`ORBIT_DIVERGENCE_THRESHOLD` during the closed
        orbit search (the absolute value of components are considered).
    """
    if max_iter is not None and max_iter <= 0:
        raise ValueError('max_iter must be greater than zero')
    x0 = backend.make_zeros(6, 1)
    if initial_guess is not None:
        x0 += initial_guess
    for i in (it.count() if max_iter is None else range(max_iter + 1)):
        x1, R = lattice.transfer_maps('reduce', order=order, indices=(0, 1), d0=x0)
        if Fs.isnan(x1).any() or (Fs.abs(x1) > ORBIT_DIVERGENCE_THRESHOLD).any():
            raise DivergingOrbitError(f'Closed orbit estimate diverged during closed orbit search: {x1}')
        error = Fs.abs(x1[:4] - x0[:4]).max()
        update = backend.zeros_like(x0)
        update[:4] += La.solve(I4 - R[:4, :4], x1[:4] - x0[:4])
        x0 = x0 + update
        # Moving the tolerance check to the end of the loop's body will perform one additional update even if the error
        # was already below the threshold (theoretically this could result in an 'x0' which yields an error larger than
        # the threshold, but expected tendency is to decrease).
        # This behavior is chosen because MADX does it that way and in some cases this extra update introduces a
        # noticeable deviation and thus causes some unit tests to fail; i.e. for comparison with MADX results we need
        # to choose the same behavior here.
        if error < tolerance:
            if return_transfer_matrix:
                return x0, lattice.transfer_maps('reduce', order=order, indices=1, d0=x0)
            else:
                return x0
    # noinspection PyUnboundLocalVariable
    raise ConvergenceError(f'Closed orbit search did not converge within {i} steps')


def linear_closed_orbit(lattice: Segment) -> TensorType:
    r"""Compute the linear closed orbit for the given lattice.

    The given lattice may contain `Element`s as well as `AlignmentError`s. Alignment errors are treated as additional
    elements that wrap the actual element: entrance transformations coming before the element, in order, and exit
    transformations being placed after, in reverse order. Hence all parts of the lattice can be described as a chain of
    linear transformations and the linear closed orbit is given as the solution to the following system of equations
    (in the transverse coordinates, for a total of :math:`n` elements (actual elements and error transformations)):

    .. math:: \left[\mathbb{1} - \bar{R}_0\right]\, x_{co} = \sum_{i=1}^{n}\bar{R}_i\,d_i

    where :math:`\bar{R}_i` is given by:

    .. math:: \bar{R}_i \equiv \prod_{j=n\\j\rightarrow j-1}^{i+1}R_j

    and :math:`R_k, d_k` are, respectively, the first and zero order term of the k-th element.

    Parameters
    ----------
    lattice : Segment

    Returns
    -------
    linear_closed_orbit : Tensor
        Tensor of shape (6,) containing the closed orbit in the transverse coordinates and zeros for the longitudinal
        coordinates.
    """
    co = backend.make_zeros(6, 1)
    d, R = lattice.transfer_maps('reduce', order=1, indices=(0, 1))
    co[:4] = La.solve(I4 - R[:4, :4], d[:4])
    return co


def transfer_maps(lattice: Segment, *,
                  method: Literal['accumulate', 'reduce', 'local'],
                  order: Literal[1, 2] = 2,
                  indices: Optional[Union[Literal[0, 1, 2], Tuple[Literal[0, 1, 2], ...]]] = None,
                  symplectify: bool = True,
                  labels: bool = False,
                  unfold_alignment_errors: bool = False
                  ) -> Union[TensorType, TransferMap, List[TensorType], List[TransferMap], List[Tuple[str, TensorType]], List[Tuple[str, TransferMap]]]:
    """Compute the transfer maps of the lattice, performing a closed orbit search beforehand and using it as the starting value.
       For details see :meth:`Segment.transfer_maps`."""
    return lattice.transfer_maps(method, order=order, indices=indices, symplectify=symplectify, labels=labels, unfold_alignment_errors=unfold_alignment_errors,
                                 d0=closed_orbit(lattice, order=order))
