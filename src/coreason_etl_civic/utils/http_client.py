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

import requests

from coreason_etl_civic.utils.logger import logger


def fetch_civic_tsv(url: str, chunk_size: int = 8192) -> Iterator[bytes]:
    """
    AGENT INSTRUCTION: Streams a file from a remote URL over HTTP GET.
    It follows redirects as per requirements.
    Yields the file content in chunks.
    """
    logger.info("Fetching CIViC TSV", url=url)
    try:
        with requests.get(url, stream=True, allow_redirects=True, timeout=30) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    yield chunk
    except requests.RequestException:
        logger.exception("Failed to fetch CIViC TSV", url=url)
        raise
