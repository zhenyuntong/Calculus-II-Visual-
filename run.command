#!/bin/bash
cd "$(dirname "$0")"
pip3 install -q flask sympy
open http://localhost:5050
python3 app.py
