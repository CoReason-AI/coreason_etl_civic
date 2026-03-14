# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic

from pydantic_settings import BaseSettings, SettingsConfigDict


class CivicSettings(BaseSettings):
    """
    AGENT INSTRUCTION: This class encapsulates configuration for the coreason_etl_civic pipeline.
    """

    civic_nightly_base_url: str = "https://civicdb.org/downloads/nightly/"
    civic_target_files: tuple[str, ...] = (
        "nightly-GeneSummaries.tsv",
        "nightly-VariantSummaries.tsv",
        "nightly-ClinicalEvidenceSummaries.tsv",
    )

    model_config = SettingsConfigDict(env_prefix="CIVIC_", env_file=".env", extra="ignore")
