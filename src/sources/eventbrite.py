import csv, json, datetime, uuid
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "out"
CFG_INT = json.load(open(ROOT / "config" / "integrations.json"))
CFG_PREF = json.load(open(ROOT / "config" / "preferences.json"))
def suggest_from_eventbrite():
    if not CFG_INT.get("eventbrite",{}).get("enabled", False): return 0
    OUT.mkdir(parents=True, exist_ok=True)
    file = OUT / "suggestions.csv"
    fields = ["_id","source","title","category","price","url","start","city","notes","match_score"]
    write_header = not file.exists()
    rows = [
      {"title":"Peninsula Food Truck Fest","category":"food & drink","price":0,"url":"https://example.com/eb1","start":"2025-08-16 12:00","city":"Hampton","notes":"family-friendly, outdoor"},
      {"title":"Acoustic Night at the Park","category":"live music","price":10,"url":"https://example.com/eb2","start":"2025-08-23 18:30","city":"Newport News","notes":"evening, picnic allowed"}
    ]
    out = []
    for m in rows:
        score = 0
        if m["category"] in CFG_PREF.get("likes_tags", []): score += 2
        if any(k in m["title"].lower() for k in ["food","truck","music","festival"]): score += 2
        if m["price"] <= CFG_PREF.get("max_price_usd", 999): score += 1
        out.append({"_id": uuid.uuid4().hex, "source":"eventbrite", **m, "match_score":score})
    with file.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if write_header: w.writeheader()
        for r in out: w.writerow(r)
    return len(out)
