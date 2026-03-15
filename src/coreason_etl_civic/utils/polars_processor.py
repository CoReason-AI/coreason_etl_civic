# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic

from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any

import polars as pl

from coreason_etl_civic.utils.identifiers import generate_coreason_id
from coreason_etl_civic.utils.logger import logger


def process_civic_tsv(
    file_stream: bytes, entity_type: str, source_id_col: str, source_file: str | None = None
) -> Iterator[dict[str, Any]]:
    """
    AGENT INSTRUCTION: Process raw CIViC TSV content using Polars.
    Expects the file content as a single bytes object for parsing.
    Generates UUIDs and wraps the output into the raw_data payload.
    Adds source_file and ingestion_ts to the output if source_file is provided.
    """
    logger.info("Processing CIViC TSV using Polars", entity_type=entity_type)
    ingestion_ts = datetime.now(tz=UTC).isoformat()

    # Load TSV from bytes
    df = pl.read_csv(file_stream, separator="\t", infer_schema_length=0, null_values=[""])

    # Determine unique IDs for mapping using map_batches
    df = df.with_columns(
        pl.col(source_id_col)
        .cast(pl.Utf8)
        .map_batches(
            lambda s: pl.Series([str(generate_coreason_id(val)) for val in s]),
            return_dtype=pl.Utf8,
        )
        .alias("coreason_id")
    )

    # Convert to dictionaries
    records = df.to_dicts()

    for row in records:
        coreason_id = row.pop("coreason_id")
        record = {
            "coreason_id": coreason_id,
            "raw_data": row,
        }
        if source_file is not None:
            record["source_file"] = source_file
            record["ingestion_ts"] = ingestion_ts
        yield record
