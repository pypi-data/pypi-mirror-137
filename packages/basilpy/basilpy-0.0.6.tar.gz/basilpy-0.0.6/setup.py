from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

requirements = ["nbformat>=4",  "requests>=2", 
                "scipy>=1","numpy>1.19","mpmath>=1.2"]

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='basilpy',
    version="0.0.6", #get_git_version_pypi(),
    packages=find_packages(),
    description='Python code to estimate the signal from an On/Off measurement'
                'with the BASiL approach [ PhysRevD.103.123001 ]',
    long_description=long_description,  # this is the readme
    long_description_content_type='text/x-rst',

    # The project's main homepage.
    url='https://github.com/giacomodamico24/basilpy',

    # Author details
    author="Giacomo D'Amico",
    author_email='giacomo.damico@uib.no',

    # Choose your license
    license='gpl-3.0',

    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    # What does your project relate to?
    keywords=['gamma-ray astronomy', 'on/off measurements','signal estimation','Bayes'],

    install_requires=requirements,

)
