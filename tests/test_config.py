# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic

import json
import os
from string import printable
from unittest import mock

from hypothesis import given
from hypothesis import strategies as st

from coreason_etl_civic.config import CivicSettings


def test_civic_settings_defaults() -> None:
    """AGENT INSTRUCTION: Ensure CivicSettings has correct default values."""
    settings = CivicSettings()
    assert settings.civic_nightly_base_url == "https://civicdb.org/downloads/nightly/"
    assert settings.civic_target_files == (
        "nightly-GeneSummaries.tsv",
        "nightly-VariantSummaries.tsv",
        "nightly-ClinicalEvidenceSummaries.tsv",
    )


@mock.patch.dict(
    os.environ,
    {
        "CIVIC_CIVIC_NIGHTLY_BASE_URL": "http://test-url.org/nightly/",
        "CIVIC_CIVIC_TARGET_FILES": '["test1.tsv", "test2.tsv"]',
    },
)
def test_civic_settings_env_override() -> None:
    """AGENT INSTRUCTION: Ensure CivicSettings loads from environment correctly."""
    settings = CivicSettings()
    assert settings.civic_nightly_base_url == "http://test-url.org/nightly/"
    assert settings.civic_target_files == ("test1.tsv", "test2.tsv")




@given(
    base_url=st.text(alphabet=printable, min_size=1).filter(lambda s: "\x00" not in s),
    target_files=st.lists(st.text(alphabet=printable, min_size=1).filter(lambda s: "\x00" not in s), min_size=1),
)
def test_civic_settings_hypothesis(base_url: str, target_files: list[str]) -> None:
    """AGENT INSTRUCTION: Ensure CivicSettings accepts arbitrary strings for dynamic configuration."""
    with mock.patch.dict(
        os.environ,
        {
            "CIVIC_CIVIC_NIGHTLY_BASE_URL": base_url,
            "CIVIC_CIVIC_TARGET_FILES": json.dumps(target_files),
        },
    ):
        settings = CivicSettings()
        assert settings.civic_nightly_base_url == base_url
        assert settings.civic_target_files == tuple(target_files)
