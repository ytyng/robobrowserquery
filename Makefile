test:
	flake8 robobrowserquery
	python setup.py test

upload:
	python setup.py sdist
	twine upload dist/*

virtualenv:
	python3 -m venv venv
