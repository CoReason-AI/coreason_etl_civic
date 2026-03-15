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

import pytest
import requests

from coreason_etl_civic.utils.http_client import fetch_civic_tsv


def test_fetch_civic_tsv_success() -> None:
    """AGENT INSTRUCTION: Ensure fetching TSV yields expected chunks correctly."""
    url = "https://example.com/file.tsv"
    expected_chunks = [b"chunk1", b"chunk2"]

    mock_response = mock.MagicMock()
    mock_response.iter_content.return_value = expected_chunks
    mock_response.raise_for_status.return_value = None

    with mock.patch("requests.get", return_value=mock_response) as mock_get:
        # Mock context manager
        mock_response.__enter__.return_value = mock_response

        chunks = list(fetch_civic_tsv(url))

        assert chunks == expected_chunks
        mock_get.assert_called_once_with(url, stream=True, allow_redirects=True, timeout=30)
        mock_response.raise_for_status.assert_called_once()


def test_fetch_civic_tsv_failure() -> None:
    """AGENT INSTRUCTION: Ensure fetch raises RequestException on HTTP error."""
    url = "https://example.com/file.tsv"

    mock_response = mock.MagicMock()
    mock_response.raise_for_status.side_effect = requests.RequestException("HTTP Error")

    with mock.patch("requests.get", return_value=mock_response):
        mock_response.__enter__.return_value = mock_response

        with pytest.raises(requests.RequestException, match="HTTP Error"):
            list(fetch_civic_tsv(url))
