from contextlib import contextmanager, nullcontext
import inspect
import itertools as it
from pathlib import Path
from pprint import pprint
import re
from runpy import run_path

import click
from click_inspect import add_options_from
from click_inspect.parser import parse_docstring
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .aux import compare_with_madx
from .backends import backend
from .build import from_file, sequence_script, Beam
from . import compute
from . import elements as dipas_elements
from .elements import HKicker, VKicker, HMonitor, VMonitor, Segment
from .madx.builder import write_command
from .madx.utils import run_file, run_orm, run_script
from .plot import plot_twiss
from .utils import TemporaryFileName


@click.group()
def cli():
    pass


def _command_with_madx_py_file_argument(group, *, name=None, arg_name='file'):
    help_text = (
        f'{arg_name.upper()} path pointing to either a MADX script or a Python script (suffix: `.py`). '
        'For a MADX script, the default `dipas.madx.parser` configuration will be used to load the contained lattice. '
        'For a Python script, that script will be executed and it must define a global name `lattice` which will be used '
        'as the lattice instance (i.e. it should be a `dipas.elements.Segment` instance). This is useful for customizing '
        'the parser and/or providing custom lattices.'
    )

    def decorator(f):
        f.__doc__ = f'{inspect.getdoc(f)}\n\n{help_text}\n'
        f = click.argument(arg_name, type=click.Path(exists=True))(f)
        return group.command(name=name)(f)

    return decorator


_HELP_OPTION_MAKETHIN = (
    'Comma-separated list of makethin specifiers with the format T:N:S '
    '(where T indicates the element type from `dipas.elements`, N is the number of slices and S is the slicing style). '
    'For example the default MADX slicing of kickers is "Kicker:2:edge".'
)


@_command_with_madx_py_file_argument(cli)
@click.option('--makethin', type=str, help=_HELP_OPTION_MAKETHIN)
@click.option('--save', type=click.Path())
@click.option('--hide', is_flag=True, default=False)
@add_options_from(plot_twiss, exclude={'data'})
def plot(file, makethin, save, hide, **kwargs):
    """Plot the given lattice and Twiss parameters."""
    lattice = _load_lattice_from_file(file)
    if makethin:
        lattice = _makethin(lattice, makethin)
    fig, __ = plot_twiss(lattice, **kwargs)
    if save:
        fig.savefig(save)
    if not hide:
        plt.show()


@_command_with_madx_py_file_argument(cli)
@click.option('--makethin', type=str, help=_HELP_OPTION_MAKETHIN)
@click.option('--outfile', type=click.Path(), help='File path to save the Twiss table')
@click.option('-v', '--verbose', count=True)
@add_options_from(compute.twiss, exclude={'initial'}, custom={'order': {'type': int}})
def twiss(file, makethin, outfile, verbose, **kwargs):
    """Compute Twiss data, print global parameters (such as tunes) and optionally save lattice functions."""
    lattice = _load_lattice_from_file(file)
    lattice.apply_unique_labels()
    if makethin:
        lattice = _makethin(lattice, makethin)
    twiss_data = compute.twiss(lattice, **kwargs)
    twiss_table = twiss_data.pop('lattice')
    if outfile is not None:
        twiss_table.applymap(lambda x: x.item()).to_csv(outfile)
    keys = {0: ('Q1', 'Q2')}.get(verbose, twiss_data.keys())
    pprint({k: twiss_data[k] for k in keys})


@_command_with_madx_py_file_argument(cli)
@click.argument('outfile', type=click.Path())
@add_options_from(compute.orm, exclude={'kickers', 'monitors'}, custom={'order': {'type': int}})
def orm(file, outfile, **kwargs):
    """Compute Orbit Response Matrix and save as CSV file."""
    lattice = _load_lattice_from_file(file)
    kickers = lattice[HKicker] + lattice[VKicker]
    h_monitor = lattice[HMonitor]
    v_monitor = lattice[VMonitor]
    monitors = h_monitor + v_monitor
    orm_data_all = compute.orm(lattice, kickers=kickers, monitors=monitors, **kwargs)
    orm_data_x = orm_data_all.x[:len(h_monitor)]
    orm_data_y = orm_data_all.y[len(h_monitor):]
    orm_data = backend.concatenate((orm_data_x, orm_data_y), dim=0)
    pd.DataFrame(
        index=[e.label for e in monitors],
        columns=[e.label for e in kickers],
        data=backend.to_numpy(orm_data),
    ).to_csv(outfile)


@cli.group()
def madx():
    """MADX subcommands (twiss and orm)."""
    pass


@madx.command('twiss')
@click.argument('file', type=click.Path(exists=True))
@click.option('--outfile', type=click.Path(), help='File path to save the Twiss table')
@add_options_from(run_script, include={'madx', 'wdir'})
def madx_twiss(file, outfile, **kwargs):
    """Use MADX to compute Twiss data, print global parameters (such as tunes) and optionally save lattice parameters."""
    if outfile is None:
        file_name_ctx = TemporaryFileName()
    else:
        file_name_ctx = nullcontext(outfile)
    with file_name_ctx as twiss_file_name:
        twiss_table, twiss_meta = run_file(file, twiss=dict(file=twiss_file_name, meta=True), **kwargs)[twiss_file_name]
    pprint(twiss_meta)
    if outfile:
        twiss_table.to_csv(outfile)


@_command_with_madx_py_file_argument(madx, name='orm')
@click.argument('outfile', type=click.Path())
@click.option('--kickers', multiple=True, help='Regex (/) or glob (*) patterns to identify kickers by their labels')
@click.option('--monitors', multiple=True, help='Regex (/) or glob (*) patterns to identify monitors by their labels')
@add_options_from(run_orm, include={'kicks', 'madx'})
def madx_orm(file, outfile, *, kickers, monitors, **kwargs):
    """Use MADX to compute Orbit Response Matrix (ORM)."""

    lattice = _load_lattice_from_file(file)

    def _select_element_labels(patterns, types):
        if patterns:
            patterns = (re.compile(p.strip('/')) if p.startswith('/') else p for p in patterns)
            elements = _select_elements_from_patterns(patterns)
        else:
            elements = (e for tp in types for e in lattice[tp])
        return [e.label for e in elements]

    def _select_elements_from_patterns(patterns):
        elements = (lattice[pattern] for pattern in patterns)
        elements = (e if isinstance(e, list) else [e] for e in elements)
        return it.chain.from_iterable(elements)

    orm_data = run_orm(file,
                       kickers=_select_element_labels(kickers, (HKicker, VKicker)),
                       monitors=_select_element_labels(monitors, (HMonitor, VMonitor)),
                       **kwargs)
    orm_data.to_csv(outfile)


@_command_with_madx_py_file_argument(cli)
@click.option('--orm/--no-orm', default=False)
@click.option('--madx', type=click.Path(exists=True))
def verify(file, *, orm, madx):
    """Verify the functionality for the given MADX script by comparing results from DiPAS to MADX."""
    lattice = _load_lattice_from_file(file)
    with section('Comparing results from DiPAS with MADX'):
        df_global, df_twiss, *other = compare_with_madx(lattice, orm=orm, madx=madx)
    with section('Global lattice parameters (difference):'):
        print(df_global.loc['dipas'] - df_global.loc['madx'])
    with section('Lattice functions (maximum difference along lattice):'):
        print(np.abs(df_twiss.loc['dipas'] - df_twiss.loc['madx']).max())
    if orm:
        df_orm, = other
        with section('ORM (maximum difference):'):
            print(np.abs(df_orm.loc['dipas'] - df_orm.loc['madx']).to_numpy().max())


@cli.group()
def convert():
    pass


@convert.group()
def to():
    pass


@_command_with_madx_py_file_argument(to)
@click.option('--outfile', type=click.Path(), help='Defaults to the script path with suffix ".html"')
@click.option('--paramodi', type=click.Path(exists=True), help='Ignored for .py scripts')
@click.option('--drift-quads/--no-drift-quads', default=False, help='Whether to plot K1=0 quads as drift spaces')
def html(file, outfile, paramodi, drift_quads):
    """Convert the given lattice definition to HTML format which can be viewed and inspected with a web browser."""
    lattice = _load_lattice_from_file(file, paramodi=paramodi)
    if outfile is None:
        outfile = Path(file).with_suffix('.html')
    with open(outfile, 'w') as fh:
        fh.write(sequence_script(lattice, markup='html', drift_quads=drift_quads))


@cli.group('print')
def print_():
    pass


def _add_print_beam_options(f):
    spec = inspect.getfullargspec(Beam)
    doc_spec = parse_docstring(Beam.__doc__.replace('Attributes', 'Parameters'))
    for parameter, default in zip(spec.args[1:], spec.defaults):
        f = click.option(
            f'--{parameter}',
            default=default,
            type=spec.annotations[parameter],
            help=doc_spec[parameter]['help'],
        )(f)
    f = click.option(
        '--as',
        type=click.Choice(['dict', 'series', 'madx'], case_sensitive=False),
        default='madx',
    )(f)
    return f


@print_.command()
@_add_print_beam_options
def beam(**kwargs):
    """Print the full list of beam properties based on user input (i.e. also compute the remaining properties)."""

    def display_style_madx(attrs):
        cmd = write_command('beam', attrs)
        return cmd.replace(', ', f',\n{4*" "}') + ';'

    display_styles = {'dict': dict, 'series': pd.Series, 'madx': display_style_madx}

    display_style = display_styles[kwargs.pop('as')]
    beam_obj = Beam(**kwargs)
    beam_obj = display_style(beam_obj.to_dict())
    printer = {str: print}.get(type(beam_obj), pprint)
    printer(beam_obj)


@contextmanager
def section(title: str, *, post_pad: str = 2*'\n'):
    print(title)
    yield
    print(end=post_pad)


def _load_lattice_from_file(file: str, *, paramodi=None, py_lattice_name='lattice'):
    file = Path(file)
    if file.suffix == '.py':
        namespace = run_path(file)
        try:
            return namespace[py_lattice_name]
        except KeyError:
            raise RuntimeError(f'{file.resolve()!s} does not define a global attribute {py_lattice_name!r}') from None
    return from_file(str(file.resolve()), paramodi=paramodi)


def _makethin(lattice: Segment, specification: str):
    n_dict = {}
    style_dict = {}
    for string in specification.split(','):
        try:
            name, n_slices, style = string.split(':')
        except ValueError:
            raise RuntimeError(f'Makethin specifier {string!r} does not have the format "T:N:S"') from None
        else:
            element_type = getattr(dipas_elements, name)
            n_dict[element_type] = int(n_slices)
            style_dict[element_type] = style
    return lattice.makethin(n_dict, style=style_dict)


if __name__ == '__main__':
    cli()
