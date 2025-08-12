import csv, json, datetime, uuid
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "out"
CFG_INT = json.load(open(ROOT / "config" / "integrations.json"))
CFG_PREF = json.load(open(ROOT / "config" / "preferences.json"))
def suggest_from_groupon():
    if not CFG_INT.get("groupon",{}).get("enabled", False): return 0
    OUT.mkdir(parents=True, exist_ok=True)
    file = OUT / "suggestions.csv"
    fields = ["_id","source","title","category","price","url","start","city","notes","match_score"]
    write_header = not file.exists()
    rows = [
      {"title":"Half-Off Dessert Flight","category":"dessert","price":12,"url":"https://example.com/gr1","start":"","city":"Hampton","notes":"voucher"},
      {"title":"Discounted Coffee Sampler","category":"coffee","price":8,"url":"https://example.com/gr2","start":"","city":"Norfolk","notes":"voucher"}
    ]
    out = []
    for m in rows:
        score = 0
        if m["category"] in CFG_PREF.get("likes_tags", []): score += 2
        if m["price"] <= CFG_PREF.get("max_price_usd", 999): score += 1
        out.append({"_id": uuid.uuid4().hex, "source":"groupon", **m, "match_score":score})
    with file.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if write_header: w.writeheader()
        for r in out: w.writerow(r)
    return len(out)
