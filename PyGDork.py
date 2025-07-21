import sys
import os
import pandas as pd
import serpapi
from dotenv import load_dotenv

load_dotenv()

def google_dork(query, api_key):
    client = serpapi.Client(api_key=api_key)
    params = {
        "engine": "google",
        "q": f"\"{query}\"",
        "num": 100
    }
    result = client.search(params)
    data = []
    for item in result.get("organic_results", []):
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        data.append({"Link": link, "Description": snippet})
    return data

def save_results(filename, data):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 PyGDork.py \"Search Term\"")
        sys.exit(1)
    query = sys.argv[1]
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("SERPAPI_KEY not found in .env file.")
        sys.exit(1)
    data = google_dork(query, api_key)
    filename = query.lower().replace(" ", "_") + ".xlsx"
    save_results(filename, data)
    print(f"Saved {len(data)} results to {filename}")
