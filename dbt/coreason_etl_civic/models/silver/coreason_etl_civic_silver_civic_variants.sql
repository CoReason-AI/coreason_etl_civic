{{ config(materialized='table') }}

WITH raw AS (
    SELECT
        coreason_id,
        raw_data,
        ingestion_ts,
        md5(raw_data::text) AS content_hash,
        ROW_NUMBER() OVER (PARTITION BY (raw_data->>'variant_id')::integer ORDER BY ingestion_ts DESC) AS rn
    FROM {{ source('bronze', 'coreason_etl_civic_bronze_civic_variants_raw') }}
)
SELECT
    coreason_id::uuid AS coreason_id,
    content_hash,
    (raw_data->>'variant_id')::integer AS variant_id,
    (raw_data->>'feature_id')::integer AS gene_id,
    raw_data->>'name' AS variant_name,
    raw_data->>'summary' AS summary
FROM raw
WHERE rn = 1
