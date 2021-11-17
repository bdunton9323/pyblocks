from setuptools import setup
from setuptools import find_packages

setup(name='pyblocks',
      version='0.1',
      description='A python clone of a famous game',
      url='https://github.com/bdunton9323/pyblocks',
      author='Benjamin Dunton',
      packages=find_packages(),
      install_requires=['wheel', 'pygame>=2.0.2', 'nose'],
      test_suite='nose.collector',
      tests_require=['nose'],
      # TODO: this is not quite right. Not sure if I even need a setup.py for this.
      scripts=['bin/pyblocks.sh'],
)