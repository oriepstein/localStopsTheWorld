import json
import sys
import re
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python add_ids_to_sights.py <file.json>")
    sys.exit(1)

file_path = Path(sys.argv[1])
city_prefix = file_path.stem.lower()

with open(file_path, "r", encoding="utf-8") as f:
    sights = json.load(f)

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text.strip())
    return text

ids_seen = set()
changed = False

for sight in sights:
    if "id" not in sight or not sight["id"]:
        base = slugify(sight["name"])
        new_id = f"{city_prefix}_{base}"

        counter = 2
        candidate = new_id
        while candidate in ids_seen:
            candidate = f"{new_id}_{counter}"
            counter += 1

        sight["id"] = candidate
        changed = True

    ids_seen.add(sight["id"])

if changed:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sights, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"IDs added to {file_path}")
else:
    print(f"No changes needed for {file_path}")
