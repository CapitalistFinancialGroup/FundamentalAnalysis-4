from setuptools import find_packages, setup

setup(
      name ='stockLibraries',
      packages = find_packages(include = ['stockLibraries']),
      version = '0.1.0',
      description = 'Fundamental Stock Analysis Libraries',
      author = 'Sudeshna Bora',
      license = 'MIT',
      install_requires = ['requests']
      )