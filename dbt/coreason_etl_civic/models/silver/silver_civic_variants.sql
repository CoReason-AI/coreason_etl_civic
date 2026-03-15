{{ config(materialized='table') }}

WITH raw AS (
    SELECT
        coreason_id,
        raw_data,
        md5(raw_data::text) AS content_hash
    FROM {{ source('bronze', 'civic_variants_raw') }}
)
SELECT
    coreason_id::uuid AS coreason_id,
    content_hash,
    (raw_data->>'variant_id')::integer AS variant_id,
    (raw_data->>'gene_id')::integer AS gene_id,
    raw_data->>'name' AS variant_name,
    raw_data->>'summary' AS summary
FROM raw
