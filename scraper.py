# scraper.py
# Free X (Twitter) listening tool using snscrape + Google Sheets
# You paste this whole code into your GitHub repo file named scraper.py

import snscrape.modules.twitter as sntwitter
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64, tempfile

# ---------- SETTINGS ----------
QUERY = os.environ.get("QUERY", "yourbrand OR #yourbrand -is:retweet")  # You can change later in GitHub Secrets
MAX_TWEETS = int(os.environ.get("MAX_TWEETS", "200"))  # Number of tweets per run
SHEET_NAME = os.environ.get("SHEET_NAME", "X Listening")  # Google Sheet name
CREDS_JSON = os.environ.get("GOOGLE_CREDS_JSON")  # Base64 JSON from Google Service Account
# --------------------------------

def get_gsheet_client(base64_json):
    """Decode the base64 Google credential and connect to Google Sheets."""
    creds_decoded = base64.b64decode(base64_json).decode("utf-8")
    t = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    t.write(creds_decoded.encode("utf-8"))
    t.close()

    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(t.name, scope)
    client = gspread.authorize(creds)
    return client

def scrape_tweets(query, max_tweets):
    """Scrape tweets based on query."""
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break
        tweets.append([
            tweet.id,
            tweet.date.isoformat(),
            tweet.user.username,
            tweet.user.displayname,
            tweet.content,
            f"https://x.com/{tweet.user.username}/status/{tweet.id}"
        ])
    return tweets

def save_to_google_sheet(client, sheet_name, rows):
    """Append scraped tweets to Google Sheet."""
    try:
        sheet = client.open(sheet_name).sheet1
    except Exception:
        sheet = client.create(sheet_name).sheet1

    # If first run, add headers
    if not sh
