.PHONY: test quality pep8 black types clean install build publish tree env

test:
	@poetry run pytest --cov .

quality: pep8 black

pep8:
	@poetry run flake8 flask_googlemaps --ignore=F403

black:
	@poetry run black -l 80 --check .

types:
	@mypy --py2 flask_googlemaps

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
