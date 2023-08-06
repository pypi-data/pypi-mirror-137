from setuptools import setup, find_packages

setup(
    name="pycomunefirenze",
    version="0.4.1",
    author="Ubaldo Puocci",
    author_email="ubaldo.puocci@comune.fi.it",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["requests", "psycopg2", "redmail"],
)
