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
