# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic

import importlib
from pathlib import Path

from coreason_etl_civic.utils.logger import logger


def test_logger_initialization() -> None:
    """Test that the logger is initialized correctly and creates the log directory."""
    import coreason_etl_civic.utils.logger

    importlib.reload(coreason_etl_civic.utils.logger)

    log_path = Path("logs")
    assert log_path.exists()
    assert log_path.is_dir()


def test_logger_exports() -> None:
    """Test that logger is exported."""
    assert logger is not None


def test_logger_directory_creation() -> None:
    """Test logger directory creation when it does not exist."""
    import importlib
    import shutil
    from pathlib import Path

    import coreason_etl_civic.utils.logger

    log_path = Path("logs")
    if log_path.exists():
        shutil.rmtree(log_path)

    importlib.reload(coreason_etl_civic.utils.logger)

    assert log_path.exists()
    assert log_path.is_dir()
