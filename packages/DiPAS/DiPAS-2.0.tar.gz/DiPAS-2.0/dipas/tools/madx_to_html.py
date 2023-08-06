"""Convert a MADX sequence script to a corresponding HTML version (for display in a web browser)."""

import argparse
import os.path
import sys
import warnings

from dipas.build import from_file, sequence_script


parser = argparse.ArgumentParser()
parser.add_argument('infile')
parser.add_argument('outfile', nargs='?', default=None)
parser.add_argument('--paramodi', default=None)
parser.add_argument('--drift-quads', action='store_true')


def main():
    warnings.warn('`madx-to-html` is deprecated; please use `dipas convert to html` instead', category=FutureWarning)
    args = parser.parse_args()
    if args.outfile is None:
        args.outfile = f'{os.path.splitext(args.infile)[0]}.html'
    with open(args.outfile, 'w') as fh:
        fh.write(sequence_script(from_file(args.infile, paramodi=args.paramodi), markup='html',
                                 drift_quads=args.drift_quads))
    return 0


if __name__ == '__main__':
    sys.exit(main())
