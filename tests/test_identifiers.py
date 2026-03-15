# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_civic

import uuid

from coreason_etl_civic.utils.identifiers import NAMESPACE_CIVIC, generate_coreason_id


def test_generate_coreason_id_deterministic() -> None:
    """AGENT INSTRUCTION: Ensure the UUIDv5 generated is consistent for the same string."""
    id1 = generate_coreason_id("123")
    id2 = generate_coreason_id("123")
    assert id1 == id2
    assert isinstance(id1, uuid.UUID)


def test_generate_coreason_id_int_and_str() -> None:
    """AGENT INSTRUCTION: Ensure int and str versions of the same ID yield the same UUIDv5."""
    id_str = generate_coreason_id("456")
    id_int = generate_coreason_id(456)
    assert id_str == id_int


def test_generate_coreason_id_namespace() -> None:
    """AGENT INSTRUCTION: Verify the namespace used is correct."""
    expected_uuid = uuid.uuid5(NAMESPACE_CIVIC, "test_id")
    assert generate_coreason_id("test_id") == expected_uuid


def test_generate_coreason_id_empty_string() -> None:
    """AGENT INSTRUCTION: Test edge case with empty string."""
    id1 = generate_coreason_id("")
    assert isinstance(id1, uuid.UUID)
