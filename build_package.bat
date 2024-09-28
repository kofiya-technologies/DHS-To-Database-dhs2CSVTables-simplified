@echo off
REM Remove old build artifacts
rd /s /q build
rd /s /q dist
rd /s /q dhs2dbhg.egg-info
del build_output.log

REM Install the package in editable mode with dev dependencies
pipenv install --dev -e .

REM Build the package (both source and wheel distribution)
python setup.py sdist bdist_wheel > build_output.log 2>&1

echo Build completed!
