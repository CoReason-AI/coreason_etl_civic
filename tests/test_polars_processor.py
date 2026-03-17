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
    tsv_content = iter([b"evidence_id\tvariant_id\n123\t456\n"])
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
    tsv_content = iter([b"evidence_id\tvariant_id\n789\t\n"])
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
    tsv_content = iter([b"evidence_id\tvariant_id\tclinical_significance\n789\t\tN/A\n"])
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
    tsv_content = iter([b"evidence_id\tvariant_id\n123\t", b"456\n"])
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


def test_process_civic_tsv_empty_batch() -> None:
    """AGENT INSTRUCTION: Ensure empty lines or empty batches are handled."""
    tsv_content = iter([b"evidence_id\tvariant_id\n"])
    entity_type = "evidence"
    source_id_col = "evidence_id"

    results = list(process_civic_tsv(tsv_content, entity_type, source_id_col))
    assert len(results) == 0


def test_process_civic_tsv_no_newline() -> None:
    """AGENT INSTRUCTION: Ensure files ending with no newline process correctly."""
    tsv_content = iter([b"evidence_id\tvariant_id\n123\t456"])
    entity_type = "evidence"
    source_id_col = "evidence_id"

    results = list(process_civic_tsv(tsv_content, entity_type, source_id_col))
    assert len(results) == 1
    assert results[0]["raw_data"] == {"evidence_id": "123", "variant_id": "456"}


def test_process_civic_tsv_whitespace_only_batch() -> None:
    """
    AGENT INSTRUCTION: Ensure batches containing only whitespace yield nothing.
    Polars treats '   ' as a valid column value for 'evidence_id' if not empty.
    To test the `not batch_bytes.strip()` case, we just feed an empty line or entirely spaces.
    """
    tsv_content = iter([b"   \n", b"   "])
    entity_type = "evidence"
    source_id_col = "evidence_id"

    results = list(process_civic_tsv(tsv_content, entity_type, source_id_col))
    assert len(results) == 0


def test_process_civic_tsv_multiple_batches() -> None:
    """
    AGENT INSTRUCTION: Ensure batch limit chunking works properly.
    Yields partially broken lines as chunks to trigger leftover logic.
    """
    tsv_content = iter(
        [b"evidence_id\tvariant_id\n", b"0\t0\n", b"1\t", b"1\n"] + [f"{i}\t{i}\n".encode() for i in range(2, 1005)]
    )

    entity_type = "evidence"
    source_id_col = "evidence_id"

    results = list(process_civic_tsv(tsv_content, entity_type, source_id_col))

    assert len(results) == 1005
    assert results[0]["raw_data"] == {"evidence_id": "0", "variant_id": "0"}
    assert results[-1]["raw_data"] == {"evidence_id": "1004", "variant_id": "1004"}


def test_process_civic_tsv_empty_bytes() -> None:
    """AGENT INSTRUCTION: Ensure empty batch yields nothing."""
    tsv_content = iter([b"  \n"])
    entity_type = "evidence"
    source_id_col = "evidence_id"

    results = list(process_civic_tsv(tsv_content, entity_type, source_id_col))
    assert len(results) == 0
