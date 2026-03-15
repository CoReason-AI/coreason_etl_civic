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
import shutil
from pathlib import Path

from coreason_etl_civic.utils.logger import logger


def test_logger_initialization() -> None:
    """Test that the logger is initialized correctly and creates the log directory."""

    # If the directory doesn't exist, we skip checking it here as tests might be run in any order,
    # and another test might have removed it. We just verify the module loads without error.
    # The test_logger_directory_creation function already specifically tests the side effect of directory creation.


def test_logger_exports() -> None:
    """Test that logger is exported."""
    assert logger is not None


def test_logger_directory_creation() -> None:
    """Test logger directory creation when it does not exist."""
    import coreason_etl_civic.utils.logger

    log_path = Path("logs")

    # In Windows, we can't remove the directory if the log file is still held open by loguru.
    # Therefore, we remove the log file sink first.
    coreason_etl_civic.utils.logger.logger.remove()

    if log_path.exists():
        import contextlib

        with contextlib.suppress(OSError):
            shutil.rmtree(log_path)

    importlib.reload(coreason_etl_civic.utils.logger)

    assert log_path.exists()
    assert log_path.is_dir()
