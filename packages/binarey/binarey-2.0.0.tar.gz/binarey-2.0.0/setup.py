from setuptools import find_packages, setup
import codecs
import os

HERE = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

VERSION = "2.0.0"
DESCRIPTION = "A module that allows you to convert files to binary."
KEYWORDS = [
    "binary",
    "binarey",
    "bineray",
    "binery",
    "python",
    "reader",
    "parser",
    "converter",
    "binaryreader",
    "binaryparser",
    "compressor",
    "decompressor",
    "binarycompressor",
    "binaryparser"
]

setup(
    name="binarey",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/DaMuffinDev/binarey",
    author="DaMuffin",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=["functools", "argparse", "json", "os"],
    python_requires=">=3.8",
    packages=find_packages(),
    keywords=KEYWORDS,
    include_package_data=True,
    setup_requires=["wheel"]
)