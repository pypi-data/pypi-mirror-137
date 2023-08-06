from setuptools import setup

__version__ = '0.0.13'

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
    description='утилиты для обоипарк',
    install_requires=[
        'aiohttp==3.8.1',
        'bs4==0.0.1',
        'lxml==4.7.1',
        'pytest-aiohttp==1.0.3',
        'pytest-asyncio==0.17.2',
    ]
)
