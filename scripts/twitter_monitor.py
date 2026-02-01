"""
Monitors Twitter/X for mentions related to HPD/NYC Housing
Posts content hooks, notifies via Slack if hits found
"""

import os
import requests

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def monitor_mentions():
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    params = {'query':'Mitchell-Lama HPD','max_results':10}
    url = "https://api.twitter.com/2/tweets/search/recent"
    r = requests.get(url, headers=headers, params=params)
    tweets = r.json().get("data")
    for tweet in tweets or []:
        requests.post(SLACK_WEBHOOK_URL, json={"text": f"New ML HPD Tweet: {tweet['text']}"})

if __name__ == "__main__":
    monitor_mentions()
