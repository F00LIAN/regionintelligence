.PHONY: init download embed training-data

# install dependencies
# install Poetry and Python dependencies
init:
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install

# download building codes
download:
	@echo "Downloading data from codes..."
	poetry run python scripts/parallel.py
	
# run the feature-pipeline and send the feature to the feature store
embed:
	@echo "Embedding text chunks into Qdrant..."
	poetry run python scripts/embed_codes_into_quadrant.py

# backfills the feature group using historical data
training-data:
	poetry run python scripts/generate_training_data.py