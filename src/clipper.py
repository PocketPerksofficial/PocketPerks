import re, os, csv, datetime, json
from pathlib import Path
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "data" / "inbox_html"
OUT = ROOT / "data" / "out"
OUT.mkdir(parents=True, exist_ok=True)

def money_number(s):
    m = re.search(r'(\$?\s*\d+(?:\.\d{1,2})?)', s)
    if m:
        raw = m.group(1).replace('$','').strip()
        try: return float(raw)
        except: return None
    return None

def guess_offer_type(text):
    t = text.lower()
    if "buy" in t and "save" in t: return "Store"
    if "off" in t and "$" in t: return "Manufacturer"
    if "%" in t: return "Percent"
    if "free" in t: return "BOGO/Free"
    return "Special"

def extract_dates(text):
    m = re.search(r'(?:end?s?|thru|through)\s*([0-9]{1,2}[/\-][0-9]{1,2}(?:[/\-][0-9]{2,4})?)', text, re.I)
    end_date = None
    if m:
        try: end_date = dateparser.parse(m.group(1)).date()
        except: pass
    return None, end_date

def load_cfg():
    p = ROOT / "config" / "stores.json"
    return json.load(open(p)) if p.exists() else {"enabled_stores": []}

def guess_retailer(text: str, source_url: str, cfg: dict) -> str:
    t = (text or "") + " " + (source_url or "")
    t = t.lower()
    for retailer in cfg.get("enabled_stores", []):
        hints = cfg.get("retailer_hints", {}).get(retailer, [])
        for h in hints:
            if h.lower() in t: return retailer
    for place in cfg.get("enabled_restaurants", []):
        hints = cfg.get("restaurant_hints", {}).get(place, [])
        for h in hints:
            if h.lower() in t: return place
    return ""

SCHEMA = ["_id","retailer","source_url","offer_title","product","brand","category",
          "offer_type","value_raw","value_numeric","unit","terms","barcode",
          "loyalty_program","stackable_with","start_date","end_date","days_left",
          "region_tags","account_email","clip_link","status","notes","created_at"]

def parse_html_file(p, cfg):
    html = p.read_text(errors="ignore")
    soup = BeautifulSoup(html, "lxml")
    candidates = []
    for tag in soup.find_all(text=True):
        t = tag.strip()
        if len(t) >= 8 and any(k in t.lower() for k in ["off","save","coupon","deal","%","bogo","free"]):
            candidates.append(t)

    import uuid
    offers = []
    for c in candidates:
        value_numeric = money_number(c)
        offer_type = guess_offer_type(c)
        _, end_date = extract_dates(c)
        days_left = ""
        if end_date: days_left = (end_date - datetime.date.today()).days
        offers.append({
            "_id": uuid.uuid4().hex,
            "retailer": guess_retailer(c, "", cfg),
            "source_url": "",
            "offer_title": c[:120],
            "product": "",
            "brand": "",
            "category": "",
            "offer_type": offer_type,
            "value_raw": c,
            "value_numeric": value_numeric if value_numeric is not None else "",
            "unit": "USD" if value_numeric is not None else "",
            "terms": "",
            "barcode": "",
            "loyalty_program": "",
            "stackable_with": "",
            "start_date": "",
            "end_date": end_date.isoformat() if end_date else "",
            "days_left": days_left,
            "region_tags": "",
            "account_email": "",
            "clip_link": "",
            "status": "new",
            "notes": f"source={p.name}",
            "created_at": datetime.datetime.now().isoformat(timespec='seconds')
        })
    return offers

def main():
    cfg = load_cfg()
    rows = []
    for file in INBOX.glob("*.html"):
        rows.extend(parse_html_file(file, cfg))
    out_file = OUT / "coupons_normalized.csv"
    with out_file.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA); w.writeheader()
        for r in rows: w.writerow(r)
    print(f"Wrote {len(rows)} rows -> {out_file}")

if __name__ == "__main__":
    main()
