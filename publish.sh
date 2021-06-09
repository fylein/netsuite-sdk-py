#!/bin/sh
rm dist/*
python3 setup.py bdist_wheel sdist
twine upload -r ucellar dist/*
