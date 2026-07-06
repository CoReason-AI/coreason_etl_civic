{{ config(materialized='table') }}

SELECT
    e.evidence_id,
    g.gene_symbol,
    v.variant_name,
    e.disease_name,
    e.drug_names,
    e.clinical_significance,
    e.evidence_type,
    e.evidence_level,
    e.evidence_rating,
    e.pubmed_id,
    e.content_hash AS evidence_hash
FROM {{ ref('coreason_etl_civic_silver_civic_evidence') }} e
JOIN {{ ref('coreason_etl_civic_silver_civic_variants') }} v ON e.variant_id = v.variant_id
JOIN {{ ref('coreason_etl_civic_silver_civic_genes') }} g ON v.gene_id = g.gene_id
