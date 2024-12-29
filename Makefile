include .env
export

PYTHON_VERSION := $(shell python -c "print(open('.python-version').read().strip())")
INSTALLED_VERSION := $(shell python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

.PHONY: \
  lint \
  start \
  build \
  down \
  login \
  update_common

# Activates the project configuration and logs in to gcloud
login:
	@gcloud config configurations activate $(PROJECT_ID)
	@gcloud auth application-default login

# Runs linters
.PHONY: lint
lint:
	@ruff check --fix
	@ruff format
	@mypy --config-file pyproject.toml .


build:
	@docker-compose build cumplo-herald --build-arg CUMPLO_PYPI_BASE64_KEY=`base64 -i cumplo-pypi-credentials.json`

start:
	@docker-compose up -d cumplo-herald

down:
	@docker-compose down

# Updates the common library
.PHONY: update-common
update-common:
	@rm -rf .venv
	@poetry cache clear --no-interaction --all cumplo-pypi
	@poetry update
