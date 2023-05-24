#!/bin/bash -e

#TODO: replace with your own package name
python setup.py sdist  # Create the source distribution package
rm -rf MyPackage.egg-info  # Remove the existing egg-info directory
mv dist/* .  # Move the distribution package to the current directory
rm -rf dist/  # Remove the dist directory
# Install the latest version of the package in the current directory
pip install $(find . -name "MyPackage*.tar.gz" | sort -V | tail -n 1)
