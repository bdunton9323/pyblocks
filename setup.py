from setuptools import setup

setup(name='pyblocks',
      version='0.1',
      description='A python clone of a famous game',
      url='https://github.com/bdunton9323/pyblocks',
      author='Benjamin Dunton',
      packages=['pyblocks'],
      test_suite='nose.collector',
      tests_require=['nose'],
)