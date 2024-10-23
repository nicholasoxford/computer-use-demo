#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r dev-requirements.txt
pre-commit install


ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY streamlit run mac_computer_demo.py
