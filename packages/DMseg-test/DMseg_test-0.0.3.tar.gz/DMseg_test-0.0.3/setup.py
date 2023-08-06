from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Python package for DMseg'
LONG_DESCRIPTION = 'Python package for DMseg'

# Setting up
setup(
  name="DMseg_test", 
  version=VERSION,
  author="aaa bbb",
  author_email="<youremail@email.com>",
  license='MIT',
  description=DESCRIPTION,
  long_description=open('README.rst').read(),
  packages=find_packages(),

  install_requires=['pandas', 'numpy'], # add any additional packages that 
  
  keywords=['python', 'DNA methylation', 'Differentially methylated regions'],
  classifiers=["Topic :: Scientific/Engineering :: Bio-Informatics"]
)
