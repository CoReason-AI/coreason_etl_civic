# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic

from unittest import mock

from coreason_etl_civic.dlt_resources import (
    _fetch_and_process,
    get_civic_evidence,
    get_civic_genes,
    get_civic_variants,
)


@mock.patch("coreason_etl_civic.dlt_resources.fetch_civic_tsv")
@mock.patch("coreason_etl_civic.dlt_resources.process_civic_tsv")
def test_get_civic_genes_resource(mock_process: mock.MagicMock, mock_fetch: mock.MagicMock) -> None:
    """AGENT INSTRUCTION: Ensure the genes resource integrates correctly."""
    mock_fetch.return_value = iter([b"gene_id\tname\n", b"1\tBRAF"])
    mock_process.return_value = [{"coreason_id": "uuid", "raw_data": {}}]

    results = list(get_civic_genes())

    assert len(results) == 1
    mock_fetch.assert_called_once()
    mock_process.assert_called_once_with(
        mock_fetch.return_value, "genes", "gene_id", source_file="nightly-GeneSummaries.tsv"
    )


@mock.patch("coreason_etl_civic.dlt_resources.fetch_civic_tsv")
@mock.patch("coreason_etl_civic.dlt_resources.process_civic_tsv")
def test_get_civic_variants_resource(mock_process: mock.MagicMock, mock_fetch: mock.MagicMock) -> None:
    """AGENT INSTRUCTION: Ensure the variants resource integrates correctly."""
    mock_fetch.return_value = iter([b"chunk"])
    mock_process.return_value = [{"coreason_id": "uuid", "raw_data": {}}]

    results = list(get_civic_variants())

    assert len(results) == 1
    mock_fetch.assert_called_once()
    mock_process.assert_called_once_with(
        mock_fetch.return_value, "variants", "variant_id", source_file="nightly-VariantSummaries.tsv"
    )


@mock.patch("coreason_etl_civic.dlt_resources.fetch_civic_tsv")
@mock.patch("coreason_etl_civic.dlt_resources.process_civic_tsv")
def test_get_civic_evidence_resource(mock_process: mock.MagicMock, mock_fetch: mock.MagicMock) -> None:
    """AGENT INSTRUCTION: Ensure the evidence resource integrates correctly."""
    mock_fetch.return_value = iter([b"chunk"])
    mock_process.return_value = [{"coreason_id": "uuid", "raw_data": {}}]

    results = list(get_civic_evidence())

    assert len(results) == 1
    mock_fetch.assert_called_once()
    mock_process.assert_called_once_with(
        mock_fetch.return_value, "evidence", "evidence_id", source_file="nightly-ClinicalEvidenceSummaries.tsv"
    )


@mock.patch("coreason_etl_civic.dlt_resources.fetch_civic_tsv")
@mock.patch("coreason_etl_civic.dlt_resources.process_civic_tsv")
def test_fetch_and_process_integration(mock_process: mock.MagicMock, mock_fetch: mock.MagicMock) -> None:
    """AGENT INSTRUCTION: Test the helper function buffering logic."""
    mock_fetch.return_value = iter([b"gene_id\tname\n", b"1\tBRAF"])
    mock_process.return_value = [{"coreason_id": "uuid", "raw_data": {"gene_id": "1", "name": "BRAF"}}]

    results = list(_fetch_and_process("http://fake.url", "genes", "gene_id", "nightly-GeneSummaries.tsv"))

    assert len(results) == 1
    mock_fetch.assert_called_once_with("http://fake.url")
    mock_process.assert_called_once_with(
        mock_fetch.return_value, "genes", "gene_id", source_file="nightly-GeneSummaries.tsv"
    )
