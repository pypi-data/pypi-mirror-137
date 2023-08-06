import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Dependencies
requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())

# This call to setup() does all the work
setup(
    name="stockmarketmba",
    version="1.0.4",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["stockmarketmba"], 
    install_requires = requirements
)