import urllib.request
import json
import datetime

# Fetch from USGS API - last 30 days, M2.5+
url = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query"
    "?format=geojson"
    "&starttime=2026-10-02"
    "&endtime=2026-11-02"
    "&minmagnitude=2.5"
    "&orderby=time"
    "&limit=5000"
)

print("Fetching USGS earthquake data...")
req = urllib.request.Request(url, headers={"User-Agent": "SeismoScope/1.0"})
with urllib.request.urlopen(req, timeout=60) as r:
    data = json.loads(r.read().decode("utf-8"))

count = len(data.get("features", []))
print(f"Fetched {count} earthquake events (M2.5+, last 30 days)")

# Save compact version
out_path = "e:/SeismoScope/data/quakes_30d.geojson"
with open(out_path, "w") as f:
    json.dump(data, f, separators=(",", ":"))
print(f"Saved to {out_path}")

# Print sample
if data["features"]:
    feat = data["features"][0]
    props = feat["properties"]
    mag = props.get("mag")
    place = props.get("place")
    print(f"Sample: M{mag} - {place}")
