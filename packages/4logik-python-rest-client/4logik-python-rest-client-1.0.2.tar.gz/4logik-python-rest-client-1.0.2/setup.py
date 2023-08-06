"""Setup script for 4logik-python-rest-client"""

# Standard library imports
import pathlib

# Third party imports
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent

# The text of the README file is used as a description
README = (HERE / "readme_for_pypi.md").read_text()

# This call to setup() does all the work
setup(
    name="4logik-python-rest-client",
    version="1.0.2",
    description="Execute microservice endpoint using HTTP REST",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.4logik.com/",
    keywords='python project',
    author="Eugenia Morales",
    author_email="eugeniamorales251@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=['py4logik_python_rest_client'],
    install_requires=["requests"],
)
