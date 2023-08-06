from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy
import os

extensions = [
    Extension("sklearn_quantile.utils.weighted_quantile",
              ["sklearn_quantile/utils/weighted_quantile.pyx"]),
    Extension("sklearn_quantile.ensemble.quantile",
              ["sklearn_quantile/ensemble/quantile.pyx"]),
    Extension("sklearn_quantile.ensemble.maximum",
              ["sklearn_quantile/ensemble/maximum.pyx"])
]

setup(
    name='sklearn_quantile',
    version='0.0.2',
    packages=find_packages(),
    url='',
    license='BSD 3 clause',
    author='Jasper Roebroek',
    author_email='roebroek.jasper@gmail.com',
    ext_modules=cythonize(extensions),
    include_dirs=[numpy.get_include()],
    setup_requires=['cython', 'numpy'],
    install_requires=['sklearn', 'numpy'],
    extras_require={
        'develop': ['cython', 'sphinx', 'sphinx_rtd_theme', 'numpydoc', 'jupyter', 'matplotlib', 'pandas']
    }
)
