install:
	poetry install
gendiff:
	poetry run gendiff
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl
package-uninstall:
	python3 -m pip uninstall hexlet_code-0.1.0-py3-none-any.whl
	
test:
	poetry run pytest

lint:
	poetry run flake8 page_loader
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

selfcheck:
	poetry check

check: selfcheck test lint