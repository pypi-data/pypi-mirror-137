
import os
from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name="NBCPU-Pipeline",
    ext_modules=cythonize("Source/*.py"),
    description="Parallel Threading Utilizing Common CPU Procedures",
    author="Alex",
    author_email="obfuscate@riseup.net"
)

for i in os.listdir('Source/'):
    if(i.endswith('.c')):
        os.remove('Source/' + i)

