# SHOULDERS-OF-GIANTS-DHS2DB-HG
TODO - Talk about the project

## Set up a new venv
Run this command to set up a new venv using the same existing Pipfile and Pipfile.lock
```commandline
pip install setuptools==68.0.0
pip install pipenv
pipenv install --deploy --ignore-pipfile
```

## How to build the Python wheel package
Before building a Python wheel package, you should install `wheel` library. Run this command to install the library
```commandline
pip install --upgrade pip setuptools
pipenv install wheel twine
```

Simply run the batch file from the command line to build the package again:
```commandline
build_package.bat
```