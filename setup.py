from distutils.core import setup

setup(
    name='ScholrRoles',
    version='0.0.21',
    author='Jorge Alpedrinha Ramos',
    author_email='jalpedrinharamos@gmail.com',
    packages=['scholrroles'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Django permissions engine.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.5",
    ],
)