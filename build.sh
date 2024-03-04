#!/usr/bin/env bash
pip install build black

black .
python3 -m build
