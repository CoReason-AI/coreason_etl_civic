# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic

import dlt

from coreason_etl_civic.dlt_resources import (
    get_civic_evidence,
    get_civic_genes,
    get_civic_variants,
)
from dlt.helpers.dbt.runner import create_runner

from coreason_etl_civic.utils.logger import logger


def run_pipeline() -> None:
    """
    AGENT INSTRUCTION: Run the full ingestion pipeline.
    Must use max_table_nesting=0 to ensure JSONB properties.
    """
    logger.info("Starting CIViC DLT Pipeline")

    pipeline = dlt.pipeline(
        pipeline_name="civic_nightly_pipeline",
        destination="postgres",
        dataset_name="bronze",
    )

    """
    Note: dlt handles max_table_nesting=0 internally if configured via config.toml.
    We explicitly inject max_table_nesting at the resource execution layer to ensure JSONB behavior.
    """
    genes = get_civic_genes()
    genes.max_table_nesting = 0

    variants = get_civic_variants()
    variants.max_table_nesting = 0

    evidence = get_civic_evidence()
    evidence.max_table_nesting = 0

    load_info = pipeline.run(
        [
            genes,
            variants,
            evidence,
        ],
    )

    logger.info("CIViC DLT Pipeline Completed", load_info=str(load_info))

    logger.info("Starting dbt transformations")
    from dlt.common.runners import Venv
    from dlt.common.destination.client import DestinationClientDwhConfiguration
    from typing import cast
    venv = Venv.restore_current()
    client_config = cast(DestinationClientDwhConfiguration, pipeline.destination_client().config)
    dbt = create_runner(
        venv,
        client_config,
        pipeline.working_dir,
        package_location="dbt/coreason_etl_civic"
    )
    dbt_results = dbt.run_all()
    logger.info("dbt transformations completed")
    for r in dbt_results:
        logger.info(f"dbt result: {r.model_name} -> {r.status}")


if __name__ == "__main__":  # pragma: no cover
    run_pipeline()
