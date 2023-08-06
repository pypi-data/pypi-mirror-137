from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'SWAT-MODFLOW model'
LONG_DESCRIPTION = 'A package that allows to work with SWAT-MODFLOW model'

# Setting up
setup(
    name="swatmf",
    version=VERSION,
    author="Seonggyu Park",
    author_email="<envpsg@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'pyemu', 'matplotlib','hydroeval', 'tqdm', 'termcolor'],
    keywords=['python', 'SWAT-MODFLOW', 'PEST'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)