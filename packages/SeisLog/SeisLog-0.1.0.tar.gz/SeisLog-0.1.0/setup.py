from setuptools import setup

setup(
    name='SeisLog',
    version='0.1.0',
    author='Samara Omar',
    author_email='somar@mines.edu',
    packages=['SeisLog'],
    url='http://pypi.python.org/pypi/SeisLog/',
    license='LICENSE.md',
    description='Extracts the seismic trace (on depth data) along some wellbore given it`s deviation survey.',
    long_description=open('README.md').read(),
    install_requires=['dask==2021.10.0','segysak','matplotlib','numpy','pandas','lasio','welly'],
    )