"""
Lead Enrichment Script

For each property row, attempts to:
- Guess property manager email/name via scraping and APIs (Hunter.io, Clearbit)
- Find phone, LinkedIn where possible
- Add AI score for pitch relevance (OpenAI/Huggingface API)

Outputs enriched CSV or updates Sheet.
"""

import os
import requests
import pandas as pd
from time import sleep
from openai import OpenAI

GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
HUNTER_IO_KEY = os.getenv('HUNTER_IO_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CLEARBIT_KEY = os.getenv('CLEARBIT_KEY')

def hunter_email_lookup(domain, company):
    res = requests.get(f"https://api.hunter.io/v2/domain-search", params=dict(
        domain=domain, company=company, api_key=HUNTER_IO_KEY
    ))
    if res.status_code == 200:
        data = res.json()
        if data.get("data", {}).get("emails"):
            return data["data"]["emails"][0].get("value", ""), data["data"]["emails"][0].get("first_name", "")
    return "", ""

def openai_relevance_score(desc):
    if not OPENAI_API_KEY:
        return 0
    prompt = f"Rate 0-10: How relevant is this apartment violation description for pitching HPD calibration? Violations: {desc}"
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
        json={
            "model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2, "max_tokens": 10,
        }
    )
    if resp.status_code == 200:
        content = resp.json()["choices"][0]["message"]["content"]
        # Extract digit score
        return int(''.join(filter(str.isdigit, content)))
    return 0

def enrich_lead_row(row):
    # Try to infer domain from address/building
    domain_guess = f"{row['Building'].replace(' ','').lower()}.com"
    pm_email, pm_name = hunter_email_lookup(domain_guess, row['Building'])
    linked_in_url = f"https://www.linkedin.com/search/results/people/?keywords={row['Building'].replace(' ','+')}+nyc+property+manager"
    phone = ""  # Could be added from an external enrichment API

    ai_score = openai_relevance_score(row.get('Violation Descriptions',''))
    return {
        "Property Manager Name": pm_name,
        "Email": pm_email,
        "Phone": phone,
        "LinkedIn": linked_in_url,
        "AI Relevance Score": ai_score
    }

def main():
    # Load sheet/CSV
    df = pd.read_csv("master_leads.csv")
    out_rows = []
    for idx, row in df.iterrows():
        enriched = enrich_lead_row(row)
        for key, val in enriched.items():
            df.at[idx, key] = val
        sleep(1)  # Prevent rate limiting
    df.to_csv("enriched_leads.csv", index=False)
    print("Enriched leads saved.")
    # Optionally, update Google Sheet here

if __name__ == "__main__":
    main()
