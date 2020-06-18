#
# Created by maks5507 (me@maksimeremeev.com)
#

from setuptools import setup, find_packages
import setuptools.command.build_py as build_py


setup_kwargs = dict(
    name='cognitive_complexity',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'nltk',
        'pymorphy2',
        'multiprocessing',
        'argparse',
        'pickle',
        'ufal.udpipe'
    ],
    setup_requires=[
    ],

    cmdclass={'build_py': build_py.build_py},
)

setup(**setup_kwargs)

