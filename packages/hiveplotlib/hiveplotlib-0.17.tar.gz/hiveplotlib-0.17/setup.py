from setuptools.config import read_configuration
from setuptools import setup

conf_dict = read_configuration("setup.cfg")
setup(**dict(**conf_dict['metadata'],**conf_dict['options']))
