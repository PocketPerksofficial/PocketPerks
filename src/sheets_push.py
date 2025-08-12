import csv, json, gspread, os
from pathlib import Path
from google.oauth2.service_account import Credentials

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "out"
CFG = json.load(open(ROOT / "config" / "sheets.json"))
SPREADSHEET_ID = os.environ.get("SHEETS_SPREADSHEET_ID", CFG["spreadsheet_id"])
SERVICE_JSON = CFG["service_account_json"]
TABS = CFG["worksheet_tabs"]
OVERWRITE = CFG.get("overwrite_tabs", True)

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(SERVICE_JSON, scopes=scope)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SPREADSHEET_ID)

def upsert_csv_to_tab(csv_path: Path, tab_name: str):
    try:
        ws = sh.worksheet(tab_name)
        if OVERWRITE:
            sh.del_worksheet(ws)
            ws = sh.add_worksheet(title=tab_name, rows="100", cols="26")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=tab_name, rows="100", cols="26")
    rows = []
    if csv_path.exists():
        with csv_path.open() as f: rows = list(csv.reader(f))
    else:
        rows = [["empty"]]
    if rows and rows[0]:
        ws.resize(rows=len(rows), cols=len(rows[0]))
        ws.update("A1", rows)
    else:
        ws.update("A1", [["empty"]])

def main():
    upsert_csv_to_tab(OUT / "coupons_normalized.csv", TABS["coupons"])
    upsert_csv_to_tab(OUT / "suggestions.csv", TABS["suggestions"])
    upsert_csv_to_tab(OUT / "master_view.csv", TABS["master"])
    print("Sheets updated.")

if __name__ == "__main__":
    main()
