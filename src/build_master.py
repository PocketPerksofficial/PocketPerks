import csv, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "out"
COUPONS = OUT / "coupons_normalized.csv"
SUGG = OUT / "suggestions.csv"
MASTER = OUT / "master_view.csv"

FIELDS = ["_id","source_type","retailer_or_venue","title","category","value_numeric","unit",
          "price","offer_type","stackable_with","terms","start_date","end_date",
          "days_left","city","region_tags","match_score","source_url","clip_link",
          "status","notes","created_at"]

def read_csv(p):
    if not p.exists(): return []
    with p.open() as f: return list(csv.DictReader(f))

def norm_coupons(rows):
    out = []
    for r in rows:
        out.append({
          "_id": r.get("_id",""),
          "source_type":"coupon",
          "retailer_or_venue":r.get("retailer",""),
          "title":r.get("offer_title",""),
          "category":r.get("category",""),
          "value_numeric":r.get("value_numeric",""),
          "unit":r.get("unit",""),
          "price":"",
          "offer_type":r.get("offer_type",""),
          "stackable_with":r.get("stackable_with",""),
          "terms":r.get("terms",""),
          "start_date":r.get("start_date",""),
          "end_date":r.get("end_date",""),
          "days_left":r.get("days_left",""),
          "city":"",
          "region_tags":r.get("region_tags",""),
          "match_score":"",
          "source_url":r.get("source_url",""),
          "clip_link":r.get("clip_link",""),
          "status":r.get("status",""),
          "notes":r.get("notes",""),
          "created_at":r.get("created_at","")
        })
    return out

def norm_sugg(rows):
    out = []
    for r in rows:
        out.append({
          "_id": r.get("_id",""),
          "source_type":"suggestion",
          "retailer_or_venue":r.get("city",""),
          "title":r.get("title",""),
          "category":r.get("category",""),
          "value_numeric":"",
          "unit":"",
          "price":r.get("price",""),
          "offer_type":"",
          "stackable_with":"",
          "terms":"",
          "start_date":r.get("start",""),
          "end_date":"",
          "days_left":"",
          "city":r.get("city",""),
          "region_tags":"",
          "match_score":r.get("match_score",""),
          "source_url":r.get("url",""),
          "clip_link":"",
          "status":"",
          "notes":r.get("notes",""),
          "created_at":datetime.datetime.now().isoformat(timespec='seconds')
        })
    return out

def main():
    rows = []
    rows += norm_coupons(read_csv(COUPONS))
    rows += norm_sugg(read_csv(SUGG))
    with MASTER.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
        for r in rows: w.writerow(r)
    print(f"Wrote {len(rows)} rows -> {MASTER}")

if __name__ == "__main__":
    main()
