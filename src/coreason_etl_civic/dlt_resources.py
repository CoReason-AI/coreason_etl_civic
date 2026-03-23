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
from typing import Any

import dlt

from coreason_etl_civic.config import CivicSettings
from coreason_etl_civic.utils.http_client import fetch_civic_tsv
from coreason_etl_civic.utils.polars_processor import process_civic_tsv


def _fetch_and_process(file_index: int, entity_type: str, source_id_col: str) -> Iterator[dict[str, Any]]:
    """
    AGENT INSTRUCTION: Common pipeline for downloading and processing TSV chunks.
    Automatically formats the URL using global CivicSettings.
    """
    settings = CivicSettings()
    filename = settings.civic_target_files[file_index]
    url = f"{settings.civic_nightly_base_url}{filename}"

    chunks = fetch_civic_tsv(url)
    yield from process_civic_tsv(chunks, entity_type, source_id_col, source_file=filename)


@dlt.resource(name="coreason_etl_civic_bronze_civic_genes_raw", write_disposition="replace")
def get_civic_genes() -> Iterator[dict[str, Any]]:
    """AGENT INSTRUCTION: Streams raw genes TSV to standard bronze schema."""
    yield from _fetch_and_process(0, "genes", "feature_id")


@dlt.resource(name="coreason_etl_civic_bronze_civic_variants_raw", write_disposition="replace")
def get_civic_variants() -> Iterator[dict[str, Any]]:
    """AGENT INSTRUCTION: Streams raw variants TSV to standard bronze schema."""
    yield from _fetch_and_process(1, "variants", "variant_id")


@dlt.resource(name="coreason_etl_civic_bronze_civic_evidence_raw", write_disposition="replace")
def get_civic_evidence() -> Iterator[dict[str, Any]]:
    """AGENT INSTRUCTION: Streams raw evidence TSV to standard bronze schema."""
    yield from _fetch_and_process(2, "evidence", "evidence_id")
