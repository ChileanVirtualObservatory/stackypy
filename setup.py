"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stackypy',
    version='0.1.1',
    description='A library to stack images of galaxies and other astronomical objects.',
    long_description=long_description,
    url='https://github.com/ChileanVirtualObservatory/stackypy',
    author = "CSRG",
    author_email = 'contact@lirae.cl',
    license='MIT', #TODO: MIT License
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
        ],
    keywords='astronomy stacking images',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['scikit-image'],
    # extras_require={
    #     'dev': [],
    #     'test': ['pyfits','matplotlib','jupyter'],
    # },
    # package_data={
    #     'sample': ['example/'],
    # },
    # data_files=[('my_data', ['data/data_file'])],
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
