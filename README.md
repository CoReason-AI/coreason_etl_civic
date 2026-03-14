# coreason_etl_civic

ETL pipeline for the Clinical Interpretation of Variants in Cancer

[![CI/CD](https://github.com/CoReason-AI/coreason_etl_civic/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/CoReason-AI/coreason_etl_civic/actions/workflows/ci-cd.yml)
[![PyPI](https://img.shields.io/pypi/v/coreason_etl_civic.svg)](https://pypi.org/project/coreason_etl_civic/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/coreason_etl_civic.svg)](https://pypi.org/project/coreason_etl_civic/)
[![License](https://img.shields.io/github/license/CoReason-AI/coreason_etl_civic)](https://github.com/CoReason-AI/coreason_etl_civic/blob/main/LICENSE)
[![Codecov](https://codecov.io/gh/CoReason-AI/coreason_etl_civic/branch/main/graph/badge.svg)](https://codecov.io/gh/CoReason-AI/coreason_etl_civic)
[![Downloads](https://static.pepy.tech/badge/coreason_etl_civic)](https://pepy.tech/project/coreason_etl_civic)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## Getting Started

### Prerequisites

- Python 3.14+
- uv

### Installation

1.  Clone the repository:
    ```sh
    git clone https://github.com/CoReason-AI/coreason_etl_civic.git
    cd coreason_etl_civic
    ```
2.  Install dependencies:
    ```sh
    uv sync --all-extras --dev
    ```

### Usage

-   Run the linter:
    ```sh
    uv run pre-commit run --all-files
    ```
-   Run the tests:
    ```sh
    uv run pytest
    ```
