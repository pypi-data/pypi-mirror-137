from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="pycomunefirenze",
    version="0.4.2",
    author="Ubaldo Puocci",
    author_email="ubaldo.puocci@comune.fi.it",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["requests", "psycopg2", "redmail"],
)
