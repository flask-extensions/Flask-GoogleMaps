.PHONY: test pep8 clean install build publish tree env

test: pep8
	py.test --cov=flask_googlemaps -l --tb=short --maxfail=1 tests/

pep8:
	@flake8 flask_googlemaps --ignore=F403

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf dist/
	@rm -rf *.egg
	@rm -rf *.egg-info

install:
	@poetry install

build:
	@poetry build

publish:
	@poetry publish

tree:
	@tree  -L 1 -a -I __pycache__ --dirsfirst --noreport

env:
	@poetry env use 3.8
