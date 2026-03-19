target_file = "/app/.venv/lib/python3.14/site-packages/mashumaro/jsonschema/models.py"

with open(target_file) as f:
    content = f.read()

new_content = content.replace("schema: Optional[str] = None", "schema: str | None = None")
with open(target_file, "w") as f:
    f.write(new_content)

print("Patched models.py")
