from pygbif import occurrences
import pandas as pd, pathlib, json

OUT = pathlib.Path("data/raw/gbif_pollinators.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

# pick species & bounding box around your sites
SPECIES = ["Bombus terrestris", "Apis mellifera"]
BBOX    = {"decimalLatitude": "51.2,51.5",   # min,max
           "decimalLongitude": "11.7,12.0"}  # min,max

rows = []
for name in SPECIES:
    res = occurrences.search(scientificName=name,
                             basisOfRecord="HUMAN_OBSERVATION",
                             has_coordinate=True,
                             **BBOX, limit=3000)   # request up to 3 000 per species
    rows.extend(res["results"])

print(f"Downloaded {len(rows)} records")
df = pd.json_normalize(rows)
df.to_csv(OUT, index=False)
print("Wrote", OUT)
