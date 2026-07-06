import mashumaro.jsonschema.models as models
path = models.__file__

with open(path, "r") as f:
    text = f.read()

# Replace the broken Python 3.14 type hint
text = text.replace("schema: Optional[str] = None", "schema: str | None = None")

with open(path, "w") as f:
    f.write(text)

print(f"Successfully patched: {path}")
