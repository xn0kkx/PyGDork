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
        "q": query,
        "num": 100
    }
    result = client.search(params)
    data = []
    for item in result.get("organic_results", []):
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        data.append({"Link": link, "Description": snippet})
    return data

def save_results(folder, filename, data):
    df = pd.DataFrame(data)
    filepath = os.path.join(folder, filename)
    df.to_excel(filepath, index=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 PyGDork.py \"Search Term\"")
        sys.exit(1)

    query = sys.argv[1]
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("SERPAPI_KEY not found in .env file.")
        sys.exit(1)

    folder_name = query.replace(" ", "_")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    social_sites = {
        "instagram": "site:instagram.com",
        "twitter": "site:twitter.com",
        "tiktok": "site:tiktok.com",
        "facebook": "site:facebook.com"
    }

    for site, dork in social_sites.items():
        search_query = f"{dork} \"{query}\""
        print(f"Searching: {search_query}")
        results = google_dork(search_query, api_key)
        filename = f"{site}_{folder_name}.xlsx"
        save_results(folder_name, filename, results)
        print(f"Saved {len(results)} results to {filename}")
