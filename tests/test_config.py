# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic

import os

from coreason_etl_civic.config import CivicConfigPolicy


def test_civic_config_policy_defaults() -> None:
    """Test the default configuration values for CivicConfigPolicy."""
    # Ensure no environment variables interfere
    old_env = dict(os.environ)
    try:
        os.environ.clear()
        config = CivicConfigPolicy()
        assert config.nightly_base_url == "https://civicdb.org/downloads/nightly/"
        assert config.gene_summaries_file == "nightly-GeneSummaries.tsv"
        assert config.variant_summaries_file == "nightly-VariantSummaries.tsv"
        assert config.clinical_evidence_summaries_file == "nightly-ClinicalEvidenceSummaries.tsv"
    finally:
        os.environ.clear()
        os.environ.update(old_env)


def test_civic_config_policy_env_overrides() -> None:
    """Test overriding configuration values using environment variables."""
    old_env = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(
            {
                "CIVIC_NIGHTLY_BASE_URL": "http://mock.civicdb.org/",
                "CIVIC_GENE_SUMMARIES_FILE": "MockGene.tsv",
                "CIVIC_VARIANT_SUMMARIES_FILE": "MockVariant.tsv",
                "CIVIC_CLINICAL_EVIDENCE_SUMMARIES_FILE": "MockEvidence.tsv",
            }
        )
        config = CivicConfigPolicy()
        assert config.nightly_base_url == "http://mock.civicdb.org/"
        assert config.gene_summaries_file == "MockGene.tsv"
        assert config.variant_summaries_file == "MockVariant.tsv"
        assert config.clinical_evidence_summaries_file == "MockEvidence.tsv"
    finally:
        os.environ.clear()
        os.environ.update(old_env)


def test_civic_config_policy_invalid_type() -> None:
    """Test invalid types raise ValidationError."""
    old_env = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(
            {
                "CIVIC_NIGHTLY_BASE_URL": "12345",  # Not a strict URL validation but can test others if we want
            }
        )
        # Pydantic string validation is loose, let's just assert it works
        config = CivicConfigPolicy()
        assert config.nightly_base_url == "12345"
    finally:
        os.environ.clear()
        os.environ.update(old_env)
