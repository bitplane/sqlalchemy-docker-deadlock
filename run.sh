#!/bin/bash

docker pull postgres

python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest --verbose test_thingy
