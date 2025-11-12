# Makefile
# This is a shortcut file for this "System" (ML API).
# Used as "make [command]".

# --- Quality ---

.PHONY: lint
lint:
	@echo "Running Linting and Formatting (Cleaning)..."
	@# We named our pre-commit (Guard) command "lint" (cleaning)
	pre-commit run --all-files

# --- Development ---

.PHONY: run
run:
	@echo "Starting API in 'development' mode (Hot Reload active)..."
	@# Our command to start the API with "reload" (automatic refresh)
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# --- Production / Packaging ---
# (Docker must be installed for these commands)

.PHONY: build
build:
	@echo "Building 'disaster-api:latest' Docker 'box' (image)..."
	@# Our command to "build" the Dockerfile
	docker build -t disaster-api:latest .

.PHONY: run-docker
run-docker:
	@echo "Running 'disaster-api:latest' 'box' (container) on port 8000..."
	@# Our command to "run" the "Box" (image)
	@# -p 8000:8000 -> (Map your computer's port 8000 -> to the Box's port 8000)
	docker run -p 8000:8000 disaster-api:latest
