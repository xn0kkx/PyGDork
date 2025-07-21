import sys
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup

def google_dork(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    urls = []
    start = 0
    while True:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote('\"' + query + '\"')}&start={start}"
        response = requests.get(search_url, headers=headers)
        if "Our systems have detected unusual traffic" in response.text:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select('a[href]')
        found = False
        for link in results:
            href = link.get("href")
            if href.startswith("/url?q="):
                url = href.split("/url?q=")[1].split("&")[0]
                urls.append(url)
                found = True
        if not found:
            break
        start += 10
        time.sleep(1)
    return urls

def save_results(filename, urls):
    with open(filename, "w") as f:
        for url in urls:
            f.write(url + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 script.py \"Search Term\"")
        sys.exit(1)
    query = sys.argv[1]
    urls = google_dork(query)
    filename = query.lower().replace(" ", "_") + ".txt"
    save_results(filename, urls)
    print(f"Saved {len(urls)} URLs to {filename}")
