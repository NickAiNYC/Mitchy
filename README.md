# Ultimate Automated Lead Generation for HPD Calibration Pitches  

## Purpose  
This repository contains a modular, serverless, AI-integrated pipeline to help NYC-based entrepreneurs pitch HPD calibration reviews to Mitchell-Lama housing properties. The system automatically identifies, enriches, and reaches out to high-priority leads, leveraging open data, automation, and machine learning for rapid, scalable outreach.

---

## Features

- **Automated Data Sourcing**: Weekly scrapes DHCR Mitchell-Lama list (https://hcr.ny.gov/mitchell-lama-housing), cross-references NYC Open Data and HUD Multifamily APIs, and outputs a master Google Sheet.
- **Lead Enrichment**: Enrich building records with property manager contacts (email, phone, LinkedIn), prioritizing urgent leads by violation analysis and AI-predicted pitch success.
- **Outreach Automation**: Connects to HubSpot, Mailchimp, Twilio, and LinkedIn for personalized drip campaigns. Monitors X (Twitter) and posts content hooks.
- **Tracking & AI Optimization**: Centralized Airtable/Google Sheets dashboard. ML-driven refinement of urgency and pitch. Slack/email alerts for important events.
- **NYC-Focused & Modular**: Handles borough quirks, designed for easy adaptation and scaling.
- **Extensible & Future-Proof**: Plug in VR/AR/Telegram modules for next-gen engagement.

---

## Repo Structure

```text
/scripts
    data_sourcing.py
    enrich_leads.py
    outreach.py
    ai_scoring.py
    optimize_ml.py
    community_bot.py
    twitter_monitor.py
/workflows
    github_scheduled.yaml
    zapier_integration.json
/docs
    README.md
    setup_guide.md
    flowcharts.md
/tests
    test_data_sourcing.py
    test_enrich_leads.py
    test_ai_scoring.py
    test_outreach.py
.env.example
Setup
Prerequisites
Github account, access to Actions
(Recommended) GCP & AWS or similar for serverless compute (or use Actions/free compute)
Google account (Sheets/OAuth, Apps Script enabled)
API keys: Socrata (NYC), HUD Multifamily, Hunter.io, Clearbit, OpenAI/HuggingFace, HubSpot, Mailchimp, Twilio, Slack
Python 3.10+ (or Node.js v18+ if using node scripts)
(Optional) Airtable, Make, Zapier, Telegram, Twitter API access
Environment Variables
Copy .env.example to .env and fill in values.
Never commit .env with secrets.

Dotenv
SOCATA_APP_TOKEN=
HUD_API_KEY=
GOOGLE_SHEET_ID=
HUNTER_IO_KEY=
CLEARBIT_KEY=
OPENAI_API_KEY=
HUBSPOT_API_KEY=
MAILCHIMP_API_KEY=
TWILIO_SID=
TWILIO_AUTH_TOKEN=
SLACK_WEBHOOK_URL=
TWITTER_BEARER_TOKEN=
AIRTABLE_API_KEY=
One-click Deploy
![Deploy to Railway](https://railway.app/button.svg)

Customize Railway template as needed with your env variables. For Airtable/Sheets/HubSpot integration, see /docs/setup_guide.md.

Workflow Overview
Mermaid
flowchart TD
    subgraph Data Sourcing
        A[Scrape DHCR ML List]
        B[NYC Open Data Violations]
        C[HUD API]
        D[Parse PDFs and Excels]
        A --> F[Merge Data]
        B --> F
        C --> F
        D --> F
        F --> G[Master Google Sheet]
    end
    subgraph Lead Enrichment
        G --> H[Contact Pull Hunter or Clearbit or Scrape]
        H --> I[AI Scoring Relevance or Urgency]
        I --> J[Enriched Sheet]
    end
    subgraph Outreach
        J --> K[CRM Import HubSpot]
        J --> L[Drip Campaigns]
        J --> M[Multi-channel Mailchimp Twilio LinkedIn X]
    end
    subgraph Tracking and Optimization
        K --> N[Dashboard Sheets or Airtable]
        N --> O[ML Feedback Loop]
        O --> I
        J --> P[Slack or Email Alerts]
    end
Quickstart
Clone the repo:
git clone https://github.com/NickAiNYC/Mitchy.git
Install Python dependencies:
pip install -r requirements.txt
Deploy GitHub Actions Workflow:
Edit /workflows/github_scheduled.yaml for your schedule.
Enable Actions.
Connect Google Sheet:
Set up OAuth credentials in /docs/setup_guide.md.
Paste your GOOGLE_SHEET_ID in .env.
Configure Outreach Integrations:
HubSpot, Mailchimp, Twilio, Slack: add API keys in .env.
See /docs/setup_guide.md for detailed steps.
Customization & Extensibility
Borough logic in /scripts/data_sourcing.py (e.g., filtering by Manhattan, Queens).
VR/AR hooks: /scripts/community_bot.py stub for immersive video call links.
Telegram module: /scripts/community_bot.py for manager group invites.
Alternative APIs: Swap out with free/public alternatives as needed.
Community & Contributing
Join the Telegram networking bot when live (/scripts/community_bot.py).
Open issues or PRs for new scripts, integrations, or enhancements.

License
MIT

