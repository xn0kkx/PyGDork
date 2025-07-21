import sys
import os
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
    urls = [item["link"] for item in result.get("organic_results", []) if item.get("link")]
    return urls

def save_results(filename, urls):
    with open(filename, "w") as f:
        for url in urls:
            f.write(url + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 PyGDork.py \"Search Term\"")
        sys.exit(1)
    query = sys.argv[1]
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("SERPAPI_KEY not found in .env file.")
        sys.exit(1)
    urls = google_dork(query, api_key)
    filename = query.lower().replace(" ", "_") + ".txt"
    save_results(filename, urls)
    print(f"Saved {len(urls)} URLs to {filename}")
