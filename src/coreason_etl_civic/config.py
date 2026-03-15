# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic

"""
AGENT INSTRUCTION: This module defines the configuration for the CIViC ETL pipeline.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CivicConfigPolicy(BaseSettings):
    """Configuration for the CIViC ETL pipeline."""

    model_config = SettingsConfigDict(env_prefix="CIVIC_", env_file=".env", env_file_encoding="utf-8")

    nightly_base_url: str = Field(
        default="https://civicdb.org/downloads/nightly/",
        description="The base URL for the CIViC nightly downloads.",
    )

    gene_summaries_file: str = Field(
        default="nightly-GeneSummaries.tsv",
        description="The filename for the Gene Summaries TSV.",
    )

    variant_summaries_file: str = Field(
        default="nightly-VariantSummaries.tsv",
        description="The filename for the Variant Summaries TSV.",
    )

    clinical_evidence_summaries_file: str = Field(
        default="nightly-ClinicalEvidenceSummaries.tsv",
        description="The filename for the Clinical Evidence Summaries TSV.",
    )
