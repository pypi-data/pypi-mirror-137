from setuptools import setup, find_packages
from akinoncli.core.version import get_version

__author__ = 'Akinon'
__license__ = 'MIT'
__maintainer__ = 'Akinon'
__email__ = 'dev@akinon.com'

VERSION = get_version()

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='akinoncli',
    version=VERSION,
    description='CLI for Akinon Cloud Commerce',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=__author__,
    author_email=__email__,
    maintainer=__maintainer__,
    maintainer_email=__email__,
    url='https://bitbucket.org/akinonteam/akinon-cli/',
    license=__license__,
    install_requires=[
        "cement==3.0.4",
        "pyyaml==6.0",
        "colorlog==6.6.0",
        "tinydb==4.3.0",
        "requests==2.25.0",
        "tabulate==0.8.7"
    ],
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'akinoncli': ['templates/*']},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Environment :: Console'
    ],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        akinoncli = akinoncli.main:main
    """,
)
