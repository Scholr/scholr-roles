from setuptools import setup, find_packages
from io import open

setup(
    name='ScholrRoles',
    version='0.1.01',
    author='Jorge Alpedrinha Ramos',
    author_email='jalpedrinharamos@gmail.com',
    packages=find_packages(),
    package_data = { '': ['*.yml']},
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Django permissions engine.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django == 1.5.1",
    ],
)