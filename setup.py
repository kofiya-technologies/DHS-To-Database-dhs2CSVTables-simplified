from setuptools import setup, find_packages

from dhs2dbhg._version import __version__


def readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


setup(
    name='dhs2dbhg',
    version=__version__,
    author='kofiyatech',
    author_email='kofiya.technologies@gmail.com',
    description="Executes the conversion of raw DHS (Demographic and Health Surveys) data into a format suitable for database storage (CSVTables).",
    url='https://kofiyatech.com/',
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=('tests', 'Private')),
    include_package_data=True,
    keywords='library package',
    install_requires=[
        "chardet",
        "pandas",
        "sqlalchemy['sqlite']",
        "werkzeug"
    ],
    python_requires='>=3.8'
)
