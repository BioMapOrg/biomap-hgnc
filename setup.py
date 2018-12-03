'''
Install script for biomap-hgnc
'''

import setuptools

VERSION = '0.0.53'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='biomap-hgnc',
    version=VERSION,
    author='Sebastian Winkler',
    author_email='winkler@informatik.uni-tuebingen.de',
    description='BioMap HGNC (HUGO Gene Nomenclature Committee) mapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BioMapOrg/biomap-hgnc',
    packages=setuptools.find_packages(),
    install_requires=[
        'biomap-core>=0.0.50',
        'biomap-utils>=0.0.51',
        'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ]
)
