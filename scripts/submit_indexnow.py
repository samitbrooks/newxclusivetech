#!/usr/bin/env python3
"""
IndexNow Protocol Submitter for Xclusive Tech
Notifies Bing, Copilot, Yahoo, Naver, and Seznam of all URLs for instant indexing.
"""

import json
import xml.etree.ElementTree as ET
import requests

HOST = "www.xclusivetech.co.ke"
KEY = "4f8e6c7d2b1a9058e34190c8a529eb71"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
INDEXNOW_API = "https://api.indexnow.org/IndexNow"

NS = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

def get_all_sitemap_urls():
    urls = []
    for sitemap in ['sitemap.xml', 'sitemap-counties.xml', 'sitemap-recheck.xml']:
        try:
            tree = ET.parse(sitemap)
            for loc in tree.findall('s:url/s:loc', NS):
                if loc.text and loc.text not in urls:
                    urls.append(loc.text)
        except Exception as e:
            print(f"Notice reading {sitemap}: {e}")
    return urls

def main():
    urls = get_all_sitemap_urls()
    print(f"Loaded {len(urls)} URLs from sitemaps.")

    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }

    print(f"Submitting {len(urls)} URLs to IndexNow API ({INDEXNOW_API})...")
    resp = requests.post(
        INDEXNOW_API,
        headers={"Content-Type": "application/json; charset=utf-8"},
        json=payload,
        timeout=30
    )

    print(f"IndexNow Response HTTP Status: {resp.status_code}")
    if resp.status_code in [200, 202]:
        print("✓ SUCCESS: URLs submitted to IndexNow. Bing and partner search engines notified for instant indexing.")
    else:
        print(f"Response Body: {resp.text}")

if __name__ == "__main__":
    main()

