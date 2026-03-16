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


def _fetch_and_process(url: str, entity_type: str, source_id_col: str, source_file: str) -> Iterator[dict[str, Any]]:
    """
    Download TSV chunks.
    Pass the generator directly to process_civic_tsv so it processes them in batches.
    """
    chunks = fetch_civic_tsv(url)
    yield from process_civic_tsv(chunks, entity_type, source_id_col, source_file=source_file)


@dlt.resource(name="civic_genes_raw", write_disposition="replace")
def get_civic_genes() -> Iterator[dict[str, Any]]:
    """AGENT INSTRUCTION: Streams raw genes TSV to standard bronze schema."""
    settings = CivicSettings()
    filename = settings.civic_target_files[0]
    url = f"{settings.civic_nightly_base_url}{filename}"
    yield from _fetch_and_process(url, "genes", "gene_id", source_file=filename)


@dlt.resource(name="civic_variants_raw", write_disposition="replace")
def get_civic_variants() -> Iterator[dict[str, Any]]:
    """AGENT INSTRUCTION: Streams raw variants TSV to standard bronze schema."""
    settings = CivicSettings()
    filename = settings.civic_target_files[1]
    url = f"{settings.civic_nightly_base_url}{filename}"
    yield from _fetch_and_process(url, "variants", "variant_id", source_file=filename)


@dlt.resource(name="civic_evidence_raw", write_disposition="replace")
def get_civic_evidence() -> Iterator[dict[str, Any]]:
    """AGENT INSTRUCTION: Streams raw evidence TSV to standard bronze schema."""
    settings = CivicSettings()
    filename = settings.civic_target_files[2]
    url = f"{settings.civic_nightly_base_url}{filename}"
    yield from _fetch_and_process(url, "evidence", "evidence_id", source_file=filename)
