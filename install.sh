#! /bin/bash

path=$(dirname $0)
cd "$path" && python3 setup.py build && python3 setup.py install --user
