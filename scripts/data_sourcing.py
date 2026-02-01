"""
Automated Data Sourcing for Mitchell-Lama HPD Pipeline

1. Scrape DHCR Mitchell-Lama list (web/PDF/Excel)
2. Cross-reference with NYC Open Data & HUD Multifamily
3. Output master Google Sheet with computed columns:
   - Building, Address, Units, Violations Count, Tier, Urgency Score
"""

import os
import time
import requests
import openpyxl
from bs4 import BeautifulSoup
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

# ENV VARS
DHCR_URL = "https://hcr.ny.gov/mitchell-lama-housing"
NYC_VIOLATIONS_URL = "https://data.cityofnewyork.us/resource/wvxf-dwi5.json"
HUD_API_URL = "https://www.huduser.gov/hudapi/public/multifamily"
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDS_JSON", "google-creds.json")

# Helper: Google Sheets setup
def get_sheets_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return build('sheets', 'v4', credentials=creds)

def write_to_sheet(data):
    service = get_sheets_service()
    sheet = service.spreadsheets()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    values = [list(data.columns)] + data.values.tolist()
    sheet.values().update(
        spreadsheetId=GOOGLE_SHEET_ID,
        range="MitchellLama!A1",
        valueInputOption="RAW",
        body={"values": values}
    ).execute()

# Step 1: Scrape DHCR site for Mitchell-Lama buildings
def scrape_dhcr_list():
    r = requests.get(DHCR_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [a['href'] for a in soup.select('a[href$=".xlsx"], a[href$=".xls"], a[href$=".pdf"]')]
    xls_links = [link for link in links if link.endswith(('.xlsx','.xls'))]
    # Fetch first Excel link
    if xls_links:
        excel_url = xls_links[0] if xls_links[0].startswith("http") else "https://hcr.ny.gov" + xls_links[0]
        df = pd.read_excel(excel_url)
        # Standardize columns
        df = df.rename(columns={
            'Building Name': 'Building',
            'Address': 'Address',
            'Number of Units': 'Units'
        })
        df = df[["Building", "Address", "Units"]]
        return df
    # TODO: Support PDF parsing
    raise Exception("No expected Excel data found on DHCR.")

# Step 2: Cross-reference with NYC Open Data (Violations)
def enrich_with_nyc_violations(df):
    # Pull all violations; ideally, filter by property
    violations_resp = requests.get(NYC_VIOLATIONS_URL, params={"$limit": 50000})
    violations = pd.DataFrame(violations_resp.json())
    violations['address'] = violations['house_number'].fillna('') + " " + violations['street_name'].fillna('')
    # Do a fuzzy join per address
    def count_violations(building_addr):
        matches = violations[violations['address'].str.lower().str.contains(building_addr.lower()[:8])]
        return len(matches), "; ".join(matches['violation_description'].dropna().unique()[:5])
    df["Violations Count"] = df["Address"].apply(lambda addr: count_violations(addr)[0])
    df["Violation Descriptions"] = df["Address"].apply(lambda addr: count_violations(addr)[1])
    return df

# Step 3: Add HUD Units data
def enrich_with_hud_units(df):
    # (Minimal stub, as API is gated; can extend)
    df["HUD Units"] = df["Units"]
    return df

# Step 4: Tiering & Urgency
def compute_tiers(df):
    df["Urgency Score"] = df["Violations Count"] * 2 + df["Units"] / 10
    df["Tier"] = pd.cut(df["Urgency Score"], [0, 10, 25, 9999], labels=[3,2,1])
    return df

def main():
    df = scrape_dhcr_list()
    print(f"Loaded {len(df)} Mitchell-Lama entries.")
    df = enrich_with_nyc_violations(df)
    df = enrich_with_hud_units(df)
    df = compute_tiers(df)
    write_to_sheet(df)
    print("Wrote to Google Sheet!")

if __name__ == "__main__":
    main()
