{{ config(materialized='table') }}

WITH raw AS (
    SELECT
        coreason_id,
        raw_data,
        md5(raw_data::text) AS content_hash
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
