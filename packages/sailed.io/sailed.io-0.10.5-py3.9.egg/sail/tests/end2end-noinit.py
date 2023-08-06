# Relative import
import sys, pathlib
sys.path.insert(1, str(pathlib.Path(__file__).parent.parent.parent.resolve()))
from sail import cli, util
import sail

import io, os
import click
import unittest
import subprocess
import requests
import json
from click.testing import CliRunner
from unittest.mock import Mock, patch

# Skip some tests if true
work_in_progress = False

# Some commands use os.execlp to pass control to the
# child process, which stops test execution after the
# spawned process exits. We can mock it and just pipe
# to a regular subprocess.
def _execlp_side_effect(*args, **kwargs):
	print(subprocess.check_output(args[1:], encoding='utf8'))

_execlp = Mock(side_effect=_execlp_side_effect)

@patch('os.execlp', _execlp)
@unittest.skipIf(__name__ != '__main__', 'Slow test, must run explicitly')
class TestEnd2End(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.runner = CliRunner(mix_stderr=False)
		# cls.fs = cls.runner.isolated_filesystem()
		# cls.fs.__enter__()
		cls.home = None

	@classmethod
	def tearDownClass(cls):
		# cls.fs.__exit__(None, None, None)
		pass

	def setUp(self):
		self.home = self.__class__.home

	def test_002_wp_home(self):
		result = self.runner.invoke(cli, ['wp', 'option', 'get', 'home'])
		self.assertEqual(result.exit_code, 0)
		self.__class__.home = result.output.strip()

	def test_019_blueprint_files(self):
		with open('/tmp/sail.files.test', 'w') as f:
			f.write('testing %s' % self.home)

		result = self.runner.invoke(cli, ['blueprint', 'test_files.yaml'])
		self.assertEqual(result.exit_code, 0)
		self.assertIn('Blueprint applied successfully', result.output)
		self.assertIn('Skipping: /tmp/does.not.exist', result.output)
		self.assertIn('Copying /tmp/sail.files.test', result.output)

		c = util.connection()
		r = c.run('cat /tmp/sail.files.test')
		self.assertIn('testing %s' % self.home, r.stdout)

		r = c.run('cat /tmp/sail.files.test.2')
		self.assertIn('testing %s' % self.home, r.stdout)

		r = c.run('cat /root/sail.files.test.3')
		self.assertIn('testing %s' % self.home, r.stdout)

		os.unlink('/tmp/sail.files.test')

if __name__ == '__main__':
	unittest.main()
