import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

# Simple trend sources (expandable)
TREND_SOURCES = {
    "google": "https://trends.google.com/trends/trendingsearches/daily?geo=US",
    "reddit": "https://www.reddit.com/r/popular.json",
    # Add more later: X via API if keys, etc.
}

def fetch_google_trends():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(TREND_SOURCES["google"], headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Parse trending searches (simplified - real impl may need API)
        trends = []
        for item in soup.select('.feed-item')[:10]:  # Adjust selector as needed
            title = item.select_one('.title')
            if title:
                trends.append(title.text.strip())
        return trends
    except:
        return ["AI tools", "side hustle", "fitness plans", "productivity", "meme templates"]  # Fallback

def fetch_reddit_trends():
    try:
        headers = {"User-Agent": "TrendDropBot"}
        response = requests.get(TREND_SOURCES["reddit"], headers=headers)
        data = response.json()
        trends = [post['data']['title'] for post in data['data']['children'][:10]]
        return trends
    except:
        return ["viral challenges", "passive income", "digital downloads"]

def get_current_trends():
    trends = fetch_google_trends() + fetch_reddit_trends()
    unique_trends = list(dict.fromkeys(trends))  # dedup
    data = {
        "timestamp": datetime.now().isoformat(),
        "trends": unique_trends[:20]
    }
    os.makedirs("data", exist_ok=True)
    with open("data/trends.json", "w") as f:
        json.dump(data, f, indent=2)
    return data

if __name__ == "__main__":
    print(get_current_trends())