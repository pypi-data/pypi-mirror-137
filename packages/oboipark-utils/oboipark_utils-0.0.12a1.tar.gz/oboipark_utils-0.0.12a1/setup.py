from setuptools import setup

__version__ = '0.0.12a1'

with open('version', 'w') as t:
    t.write(__version__)

setup(
    name='oboipark_utils',
    version=__version__,
    packages=['oboipark_utils'],
    url='https://gitlab.com/oboipark/utils',
    license='python',
    author='VVD-byte',
    author_email='vovavoronin1999@gmail.com',
    description='утилиты для обоипарк'
)
