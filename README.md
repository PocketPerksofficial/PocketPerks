# PocketPerks — Codespaces Edition
**Tagline:** Tap. Save. Repeat.

Open in **GitHub Codespaces**, run `/src` scripts, and push to Google Sheets.

## First-time
Add repo **Actions Secrets**:
- `SHEETS_SPREADSHEET_ID` — your Google Sheet ID
- `GOOGLE_CREDENTIALS_JSON` — full contents of your Service Account JSON

## Run in Codespaces
```bash
python src/clipper.py
python src/build_master.py
# optional (if enabled in config/integrations.json)
python src/suggest.py
python src/sheets_push.py
```

## Weekly automation
`.github/workflows/pocketperks-weekly.yml` runs Sundays 9am ET and pushes to Google Sheets.
