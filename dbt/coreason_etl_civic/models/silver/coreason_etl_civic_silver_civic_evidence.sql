{{ config(materialized='table') }}

WITH raw AS (
    SELECT
        coreason_id,
        raw_data,
        ingestion_ts,
        md5(raw_data::text) AS content_hash,
        ROW_NUMBER() OVER (PARTITION BY (raw_data->>'evidence_id')::integer ORDER BY ingestion_ts DESC) AS rn
    FROM {{ source('bronze', 'coreason_etl_civic_bronze_civic_evidence_raw') }}
)
SELECT
    coreason_id::uuid AS coreason_id,
    content_hash,
    (raw_data->>'evidence_id')::integer AS evidence_id,
    (raw_data->>'variant_id')::integer AS variant_id,
    NULLIF(TRIM(raw_data->>'disease'), '') AS disease_name,
    string_to_array(NULLIF(TRIM(raw_data->>'drugs'), ''), ', ') AS drug_names,
    NULLIF(TRIM(raw_data->>'evidence_type'), '') AS evidence_type,
    NULLIF(TRIM(raw_data->>'evidence_level'), '') AS evidence_level,
    NULLIF(TRIM(raw_data->>'clinical_significance'), '') AS clinical_significance,
    NULLIF(TRIM(raw_data->>'rating'), '')::integer AS evidence_rating,
    NULLIF(TRIM(raw_data->>'pubmed_id'), '') AS pubmed_id
FROM raw
WHERE rn = 1
