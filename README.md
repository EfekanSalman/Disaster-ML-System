# 🌋 Disaster-ML-System

This project is an end-to-end example of the transition from a simple **"ML Pipeline" (Jupyter Notebook)** demo to a **"Production-Level ML System"**, based on the principles of the **Modern ML Engineer Manifesto**.

The project's goal is to build a packaged (Docker) and *clean* (audited with pre-commit) API capable of serving **multiple models** (Regression, Classification, Time Series) simultaneously, using **System Thinking** and **Engineering Quality** principles — starting from a single `.csv` file.

---

## 🚀 System Capabilities (API Endpoints)

This "System" serves three distinct "products" (Problem 1, 2, 3) using EM-DAT disaster data:

1. **Regression (Damage Prediction):** `POST /predict_damage`

   * Takes inputs such as a disaster's `Total Deaths` and `Continent`, and returns the `Total Damages` (Estimated Financial Loss).
   * **Model:** `damage_model_v1.joblib` (RandomForestRegressor)

2. **Classification (Type Prediction):** `POST /predict_subgroup`

   * Takes disaster inputs and returns a prediction of the `Disaster Subgroup` (e.g., *Hydrological*, *Geophysical*).
   * **Model:** `classification_model_v1.joblib` (RandomForestClassifier)

3. **Time Series (Frequency Prediction):** `POST /predict_timeseries`

   * Takes a future `N` month period and returns the monthly frequency (count) forecast of `Flood` disasters in the Asia continent.
   * **Model:** `timeseries_model_v1.json` (Prophet)

---

## 🛠️ Technology and Philosophy (Tech Stack & Manifesto)

This project focuses on **System Quality** over **Model Score**.

| Category                  | Tools / Principles                                 |
| ------------------------- | -------------------------------------------------- |
| **API & System**          | FastAPI (with Uvicorn)                             |
| **Model Frameworks**      | Scikit-learn, Prophet                              |
| **Data "Contract"**       | Pydantic (API schema validation in `src/schemas/`) |
| **Packaging**             | Docker & Dockerfile                                |
| **Dependency Management** | `pip freeze > requirements.txt`                    |
| **Code Quality (CI)**     | pre-commit (Black & Ruff)                          |
| **Usability**             | Makefile (shortcuts for all commands)              |
| **Architecture**          | Professional repo structure (Manifesto 3)          |

---

## 🗂️ Project Structure (Manifesto 3)

This repository follows the **System Thinking** architecture:

```
DISASTERS/
│
├── models/                      # 3 trained models (.joblib & .json)
│   ├── classification_model_v1.joblib
│   ├── damage_model_v1.joblib
│   └── timeseries_model_v1.json
│
├── notebooks/                   # 01 - 08: Prototyping (EDA, Debugging, Model Training)
│
├── src/                         # The "System's" brain (Production API code)
│   ├── __init__.py
│   ├── main.py                  # FastAPI app (loads 3 models, 3 endpoints)
│   │
│   ├── processing/              # Custom data processing (Clean Code)
│   │   ├── __init__.py
│   │   ├── classification.py    # Cleaner for Problem 2
│   │   └── features.py          # Cleaner for Problem 1
│   │
│   └── schemas/                 # Pydantic data "contracts"
│       ├── __init__.py
│       ├── damage.py            # Problem 1 & 2 schemas
│       └── timeseries.py        # Problem 3 schemas
│
├── .gitignore
├── .pre-commit-config.yaml       # "Guard" rules for clean commits
├── Dockerfile                    # Instructions for the container build
├── Makefile                      # Shortcut commands (make run, make lint...)
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

---

## 🏁 Getting Started

Use the `Makefile` shortcuts to run this "System" on your local machine.

### 1. Prerequisites

* [Git](https://git-scm.com/downloads)
* [Python 3.10+](https://www.python.org/downloads/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) *(Only required for Docker mode)*

---

### 2. Setup (Development Mode)

To develop on the system (e.g., editing notebooks or API code):

```bash
# 1. Clone the project
git clone https://github.com/YOUR_USERNAME/Disaster-ML-System.git
cd Disaster-ML-System

# 2. Set up and activate the virtual environment
# (Linux/MacOS)
python3 -m venv .venv
source .venv/bin/activate

# (Windows)
python -m venv .venv
.venv\Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Install the "Guard" (pre-commit)
pre-commit install
```

---

### 3. Running the "System" (API)

#### 🧪 Development Mode

This mode uses **Hot Reload** (server restarts automatically on code save).

```bash
# Start the API
make run
```

Once started, Uvicorn will output:

```
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### 🐳 Production Mode (Docker)

Run the system inside an isolated Docker container:

```bash
# 1. Build the Docker image
make build

# 2. Run the container
make run-docker
```

---

### 4. Using the API

While the system is running (either via `make run` or `make run-docker`):

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Check:** [http://localhost:8000/](http://localhost:8000/)

You can interactively test:

* `POST /predict_damage`
* `POST /predict_subgroup`
* `POST /predict_timeseries`

---

### 5. Code Quality (Pre-Commit Checks)

Before committing any code, ensure all files are clean:

```bash
# Run the guard manually
make lint
```

This runs **Black** (formatter) and **Ruff** (linter) on all source files.

---

## 🌟 Philosophy

> "A model is temporary.
> A system is permanent."

This repository embodies the **shift from pipeline thinking → system thinking**,
where the focus is not only on *accuracy*, but on **reliability, modularity, and clarity**.
