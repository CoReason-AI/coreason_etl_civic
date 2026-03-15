# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic


from coreason_etl_civic.utils.identifiers import generate_coreason_id
from coreason_etl_civic.utils.polars_processor import process_civic_tsv


def test_process_civic_tsv_valid_input() -> None:
    """AGENT INSTRUCTION: Ensure valid TSV input yields correctly structured generator using Polars."""
    tsv_content = b"evidence_id\tvariant_id\n123\t456\n"
    entity_type = "evidence"
    source_id_col = "evidence_id"

    results = list(process_civic_tsv(tsv_content, entity_type, source_id_col))

    assert len(results) == 1
    expected_coreason_id = str(generate_coreason_id("123"))
    assert results[0] == {
        "coreason_id": expected_coreason_id,
        "raw_data": {"evidence_id": "123", "variant_id": "456"},
    }


def test_process_civic_tsv_empty_values() -> None:
    """AGENT INSTRUCTION: Ensure TSV handles empty string representation correctly."""
    tsv_content = b"evidence_id\tvariant_id\n789\t\n"
    entity_type = "evidence"
    source_id_col = "evidence_id"

    results = list(process_civic_tsv(tsv_content, entity_type, source_id_col))

    assert len(results) == 1
    expected_coreason_id = str(generate_coreason_id("789"))
    assert results[0] == {
        "coreason_id": expected_coreason_id,
        "raw_data": {"evidence_id": "789", "variant_id": None},
    }


def test_process_civic_tsv_na_values() -> None:
    """AGENT INSTRUCTION: Ensure TSV handles 'N/A' string representation correctly as null."""
    tsv_content = b"evidence_id\tvariant_id\tclinical_significance\n789\t\tN/A\n"
    entity_type = "evidence"
    source_id_col = "evidence_id"

    results = list(process_civic_tsv(tsv_content, entity_type, source_id_col))

    assert len(results) == 1
    expected_coreason_id = str(generate_coreason_id("789"))
    assert results[0] == {
        "coreason_id": expected_coreason_id,
        "raw_data": {"evidence_id": "789", "variant_id": None, "clinical_significance": None},
    }


def test_process_civic_tsv_with_source_file() -> None:
    """AGENT INSTRUCTION: Ensure process_civic_tsv adds source_file and ingestion_ts if source_file is provided."""
    tsv_content = b"evidence_id\tvariant_id\n123\t456\n"
    entity_type = "evidence"
    source_id_col = "evidence_id"
    source_file = "nightly-ClinicalEvidenceSummaries.tsv"

    results = list(process_civic_tsv(tsv_content, entity_type, source_id_col, source_file))

    assert len(results) == 1
    expected_coreason_id = str(generate_coreason_id("123"))

    assert "source_file" in results[0]
    assert results[0]["source_file"] == source_file
    assert "ingestion_ts" in results[0]

    assert results[0]["coreason_id"] == expected_coreason_id
    assert results[0]["raw_data"] == {"evidence_id": "123", "variant_id": "456"}
