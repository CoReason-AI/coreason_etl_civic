{{ config(materialized='table') }}

WITH raw AS (
    SELECT
        coreason_id,
        raw_data,
        ingestion_ts,
        md5(raw_data::text) AS content_hash,
        ROW_NUMBER() OVER (PARTITION BY (raw_data->>'gene_id')::integer ORDER BY ingestion_ts DESC) AS rn
    FROM {{ source('bronze', 'civic_genes_raw') }}
)
SELECT
    coreason_id::uuid AS coreason_id,
    content_hash,
    (raw_data->>'gene_id')::integer AS gene_id,
    raw_data->>'name' AS gene_symbol,
    raw_data->>'entrez_id' AS entrez_id,
    raw_data->>'description' AS description
FROM raw
WHERE rn = 1
