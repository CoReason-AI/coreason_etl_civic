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

# AGENT INSTRUCTION: The CIViC namespace must be a deterministic constant UUID.
NAMESPACE_CIVIC = uuid.UUID("3696f5b2-320c-4034-934c-619da0e7dc20")


def generate_coreason_id(source_id: str | int) -> uuid.UUID:
    """
    AGENT INSTRUCTION: Compute deterministic UUIDv5 for a given CIViC source ID.
    Must ensure consistent typing for the text seed.
    """
    return uuid.uuid5(NAMESPACE_CIVIC, str(source_id))
