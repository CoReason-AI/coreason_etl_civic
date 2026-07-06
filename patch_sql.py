import os

paths = [
    "dbt/coreason_etl_civic/models/silver/coreason_etl_civic_silver_civic_genes.sql",
    "dbt/coreason_etl_civic/models/silver/coreason_etl_civic_silver_civic_variants.sql"
]

for p in paths:
    if os.path.exists(p):
        with open(p, "r") as f:
            sql = f.read()
        
        # Gracefully support both V1 (gene_id) and V2 (feature_id) CIViC schemas
        sql = sql.replace(
            "raw_data->>'gene_id'", 
            "COALESCE(raw_data->>'gene_id', raw_data->>'feature_id')"
        )
        
        with open(p, "w") as f:
            f.write(sql)
        print(f"✅ Patched {p}")
