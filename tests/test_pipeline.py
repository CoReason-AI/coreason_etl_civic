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

from coreason_etl_civic.pipeline import run_pipeline


@mock.patch("coreason_etl_civic.pipeline.dlt")
@mock.patch("coreason_etl_civic.pipeline.get_civic_genes")
@mock.patch("coreason_etl_civic.pipeline.get_civic_variants")
@mock.patch("coreason_etl_civic.pipeline.get_civic_evidence")
def test_run_pipeline(
    mock_evidence: mock.MagicMock,
    mock_variants: mock.MagicMock,
    mock_genes: mock.MagicMock,
    mock_dlt: mock.MagicMock,
) -> None:
    """AGENT INSTRUCTION: Ensure the DLT pipeline runs and applies nesting rules."""
    mock_pipeline = mock.MagicMock()
    mock_dlt.pipeline.return_value = mock_pipeline
    mock_pipeline.run.return_value = "Success"

    mock_g_instance = mock.MagicMock()
    mock_genes.return_value = mock_g_instance

    mock_v_instance = mock.MagicMock()
    mock_variants.return_value = mock_v_instance

    mock_e_instance = mock.MagicMock()
    mock_evidence.return_value = mock_e_instance

    run_pipeline()

    mock_dlt.pipeline.assert_called_once_with(
        pipeline_name="civic_nightly_pipeline",
        destination="postgres",
        dataset_name="bronze",
    )

    assert mock_g_instance.max_table_nesting == 0
    assert mock_v_instance.max_table_nesting == 0
    assert mock_e_instance.max_table_nesting == 0

    mock_pipeline.run.assert_called_once_with([mock_g_instance, mock_v_instance, mock_e_instance])
