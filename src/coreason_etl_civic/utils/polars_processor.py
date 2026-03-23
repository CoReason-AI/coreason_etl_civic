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
    file_stream: Iterator[bytes], entity_type: str, source_id_col: str, source_file: str | None = None
) -> Iterator[dict[str, Any]]:
    """
    AGENT INSTRUCTION: Process raw CIViC TSV content using Polars.
    Expects an iterator of bytes representing lines or chunks.
    Processes them in batches using Polars read_csv. Lines are buffered by the newline
    character to guarantee atomic rows and prevent data splitting mid-way across batches.
    Any un-terminated bytes are preserved as leftover and prefixed to subsequent chunks.
    Empty payloads or sequences containing only whitespace are explicitly bypassed.
    Generates UUIDs and wraps the output into the raw_data payload.
    Adds source_file and ingestion_ts to the output if source_file is provided.
    """
    logger.info("Processing CIViC TSV using Polars", entity_type=entity_type)
    ingestion_ts = datetime.now(tz=UTC).isoformat()

    batch_size = 1000
    lines_buffer: list[bytes] = []
    header: bytes | None = None

    def _process_batch(batch_lines: list[bytes]) -> Iterator[dict[str, Any]]:
        """
        AGENT INSTRUCTION: Transmute the batched list of raw byte-lines into parsed payload representations.
        Validates payload length, decodes TSV schemas utilizing Polars read_csv, and synthesizes immutable
        UUID deterministic identity anchors (coreason_id) using parallel map_batches.
        Converts final frames into explicit Bronze mapping topologies.
        """
        batch_bytes = b"".join(batch_lines)
        if not batch_bytes.strip():
            return

        df = pl.read_csv(batch_bytes, separator="\t", infer_schema_length=0, null_values=["", "N/A"], truncate_ragged_lines=True)

        df = df.with_columns(
            pl.col(source_id_col)
            .cast(pl.Utf8)
            .map_batches(
                lambda s: pl.Series([str(generate_coreason_id(val)) for val in s]),
                return_dtype=pl.Utf8,
            )
            .alias("coreason_id")
        )

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

    leftover = b""
    for chunk in file_stream:
        data = leftover + chunk
        lines = data.splitlines(keepends=True)

        leftover = (lines.pop() if lines else b"") if not data.endswith(b"\n") and not data.endswith(b"\r") else b""

        for line in lines:
            if header is None:
                header = line
                continue

            lines_buffer.append(line)

            if len(lines_buffer) >= batch_size:
                yield from _process_batch([header, *lines_buffer])
                lines_buffer.clear()

    if leftover:
        lines_buffer.append(leftover)

    if lines_buffer and header is not None:
        yield from _process_batch([header, *lines_buffer])
