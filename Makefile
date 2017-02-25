#!/bin/bash

PYTHON=env/bin/python
PIP=env/bin/pip

REQUIREMENTS=requirements.txt

# Initializes the virtualenv, and installs requirements
init:
    # initialize the virtualenv
	python3 -m venv env;
    # install all dependecies
	${PIP} install --upgrade -r ${REQUIREMENTS};
	
install:
	${PIP} install --upgrade $(filter-out $@,$(MAKECMDGOALS));
	${PIP} freeze > ${REQUIREMENTS}

pip:
	${PIP} $(filter-out $@,$(MAKECMDGOALS));

python:
	${PYTHON} $(filter-out $@,$(MAKECMDGOALS));
