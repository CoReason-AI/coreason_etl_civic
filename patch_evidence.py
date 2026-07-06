import os

p = "dbt/coreason_etl_civic/models/silver/coreason_etl_civic_silver_civic_evidence.sql"
if os.path.exists(p):
    with open(p, "r") as f:
        sql = f.read()
    
    # Gracefully fallback to molecular_profile_id if variant_id is missing
    sql = sql.replace(
        "raw_data->>'variant_id'", 
        "COALESCE(raw_data->>'variant_id', raw_data->>'molecular_profile_id')"
    )
    
    with open(p, "w") as f:
        f.write(sql)
    print(f"✅ Patched {p}")
