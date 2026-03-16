import re

with open("tests/test_pipeline.py", "r") as f:
    content = f.read()

new_content = content.replace(
    """@mock.patch("coreason_etl_civic.pipeline.dlt")""",
    """@mock.patch("coreason_etl_civic.pipeline.create_runner")\n@mock.patch("coreason_etl_civic.pipeline.dlt")"""
)

new_content = new_content.replace(
    """def test_run_pipeline(
    mock_evidence: mock.MagicMock,
    mock_variants: mock.MagicMock,
    mock_genes: mock.MagicMock,
    mock_dlt: mock.MagicMock,
) -> None:""",
    """def test_run_pipeline(
    mock_evidence: mock.MagicMock,
    mock_variants: mock.MagicMock,
    mock_genes: mock.MagicMock,
    mock_dlt: mock.MagicMock,
    mock_create_runner: mock.MagicMock,
) -> None:"""
)

old_body_end = """    mock_pipeline.run.assert_called_once_with([mock_g_instance, mock_v_instance, mock_e_instance])"""

new_body_end = """    mock_pipeline.run.assert_called_once_with([mock_g_instance, mock_v_instance, mock_e_instance])

    mock_pipeline.destination_client.assert_called_once()

    mock_create_runner.assert_called_once_with(
        mock.ANY,
        mock_pipeline.destination_client.return_value.config,
        mock_pipeline.working_dir,
        package_location="dbt/coreason_etl_civic"
    )

    mock_runner = mock_create_runner.return_value
    mock_runner.run_all.assert_called_once()"""

new_content = new_content.replace(old_body_end, new_body_end)

new_content = new_content.replace(
    """    mock_e_instance = mock.MagicMock()
    mock_evidence.return_value = mock_e_instance

    run_pipeline()""",
    """    mock_e_instance = mock.MagicMock()
    mock_evidence.return_value = mock_e_instance

    mock_result = mock.MagicMock()
    mock_result.model_name = "test_model"
    mock_result.status = "success"
    mock_create_runner.return_value.run_all.return_value = [mock_result]

    run_pipeline()"""
)

with open("tests/test_pipeline.py", "w") as f:
    f.write(new_content)
