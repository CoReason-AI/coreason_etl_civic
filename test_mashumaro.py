import sys
from dataclasses import dataclass

print(sys.version)


@dataclass
class JSONObjectSchema:
    schema: str | None = None


print("OK")
