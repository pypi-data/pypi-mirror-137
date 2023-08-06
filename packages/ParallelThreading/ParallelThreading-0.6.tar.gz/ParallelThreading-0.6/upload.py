from distutils.core import setup
from gzip import READ
import pathlib
from setuptools import setup

localPath = pathlib.Path(__file__).parent
README = (localPath / "readme.md").read_text()

setup(
  name = 'ParallelThreading',         # How you named your package folder (MyLib)
  packages = ['ParallelThreading'],   # Chose the same as "name"
  version = '0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Parallel Process Threading',   # Give a short description about your library
  long_description= README,
  author = 'Python Alex',                   # Type in your name
  author_email = 'obfuscate@riseup.net',      # Type in your E-Mail
  keywords=['parallel', 'nonblocking', 'closeasync', 'threading', 'processing', 'cpu', 'python', 'processes'],
  url = 'https://github.com/user/Python-Alex',   # Provide either the link to your github or to your website
)