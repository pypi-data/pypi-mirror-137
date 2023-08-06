from ast import literal_eval
from importlib import resources
import os
import unittest

import click
from click.testing import CliRunner

from dipas.build import Beam
from dipas.cli import cli, plot, twiss, orm, madx_twiss, madx_orm
import dipas.test.sequences


class TestPlot(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['plot', str(f_path), '--save', 'fig.png', '--hide'])
                self.assertFalse(result.exception)
                self.assertEqual(result.exit_code, 0)
                self.assertTrue(os.path.exists('fig.png'))


class TestTwiss(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['twiss', str(f_path), '--outfile', 'twiss.csv'])
                self.assertFalse(result.exception)
                self.assertEqual(result.exit_code, 0)
                self.assertTrue(os.path.exists('twiss.csv'))


class TestORM(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['orm', str(f_path), 'orm.csv'])
                self.assertFalse(result.exception)
                self.assertEqual(result.exit_code, 0)
                self.assertTrue(os.path.exists('orm.csv'))


MADX = os.path.expanduser('~/bin/madx')


class TestMADXTwiss(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['madx', 'twiss', str(f_path), '--outfile', 'twiss.csv', '--madx', MADX])
                self.assertFalse(result.exception)
                self.assertEqual(result.exit_code, 0)
                self.assertTrue(os.path.exists('twiss.csv'))


class TestMADXORM(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['madx', 'orm', str(f_path), 'orm.csv', '--madx', MADX])
                self.assertFalse(result.exception)
                self.assertEqual(result.exit_code, 0)
                self.assertTrue(os.path.exists('orm.csv'))


class TestPrintBeam(unittest.TestCase):
    def test(self):
        beam = Beam(particle='proton', energy=1)
        runner = CliRunner()
        result = runner.invoke(cli, ['print', 'beam', '--particle', beam.particle, '--energy', beam.energy, '--as', 'dict'])
        self.assertFalse(result.exception)
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual(literal_eval(result.stdout), beam.to_dict())


class TestConvertToHtml(unittest.TestCase):
    def test(self):
        runner = CliRunner()
        with resources.path('dipas.test.sequences', 'sis18.seq') as f_path:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['convert', 'to', 'html', str(f_path), '--outfile', 'out.html'])
                self.assertFalse(result.exception)
                self.assertEqual(result.exit_code, 0)
                self.assertTrue(os.path.exists('out.html'))


if __name__ == '__main__':
    unittest.main()
