lint:
	flake8 smithnormalform
	flake8 test
	flake8 *.py

test: clean-pyc
	pytest
	
clean-pyc:
	rm -f *.pyc
	rm -f smithnormalform/*.pyc
	rm -f test/*.pyc

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clean: clean-pyc clean-build

build: clean lint test
	python3 setup.py sdist bdist_wheel
