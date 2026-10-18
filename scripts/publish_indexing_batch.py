#!/usr/bin/env python3
"""
Batch Google Indexing API Publisher for Xclusive Tech
Publishes high-priority crawl notifications for unindexed and updated pages.
"""

import os
import sys
import time
import json
import requests
from search_console import get_access_token, publish_indexing_url

PRIORITY_URLS = [
    # Legal pages needing recrawl to clear old noindex tags
    "https://www.xclusivetech.co.ke/privacy",
    "https://www.xclusivetech.co.ke/terms",

    # Core authority pages with updated internal linking
    "https://www.xclusivetech.co.ke/",
    "https://www.xclusivetech.co.ke/pricing",
    "https://www.xclusivetech.co.ke/services",
    "https://www.xclusivetech.co.ke/locations/",

    # Unindexed or top search query blogs
    "https://www.xclusivetech.co.ke/blog/best-web-design-companies-in-kenya",
    "https://www.xclusivetech.co.ke/blog/how-much-does-a-website-cost-in-kenya",
    "https://www.xclusivetech.co.ke/blog/how-much-does-social-media-management-cost-in-kenya",
    "https://www.xclusivetech.co.ke/blog/web-design-for-businesses-in-kiambu-county",
    "https://www.xclusivetech.co.ke/blog/ecommerce-web-design-for-solar-and-renewable-energy-companies-in-kenya",
    "https://www.xclusivetech.co.ke/blog/fresh-produce-and-grocery-ecommerce-in-kenya-delivery-logistics",
    "https://www.xclusivetech.co.ke/blog/web-design-for-cbos-and-community-organisations-in-kenya",
    "https://www.xclusivetech.co.ke/blog/how-to-build-a-successful-job-board-website-in-kenya",
    "https://www.xclusivetech.co.ke/blog/multi-currency-ecommerce-kenya-selling-to-the-diaspora",

    # All 47 County Landing Pages
    "https://www.xclusivetech.co.ke/locations/web-design-nairobi",
    "https://www.xclusivetech.co.ke/locations/web-design-kiambu",
    "https://www.xclusivetech.co.ke/locations/web-design-mombasa",
    "https://www.xclusivetech.co.ke/locations/web-design-nakuru",
    "https://www.xclusivetech.co.ke/locations/web-design-kisumu",
    "https://www.xclusivetech.co.ke/locations/web-design-uasin-gishu",
    "https://www.xclusivetech.co.ke/locations/web-design-machakos",
    "https://www.xclusivetech.co.ke/locations/web-design-kajiado",
    "https://www.xclusivetech.co.ke/locations/web-design-kilifi",
    "https://www.xclusivetech.co.ke/locations/web-design-kwale",
    "https://www.xclusivetech.co.ke/locations/web-design-meru",
    "https://www.xclusivetech.co.ke/locations/web-design-nyeri",
    "https://www.xclusivetech.co.ke/locations/web-design-kakamega",
    "https://www.xclusivetech.co.ke/locations/web-design-kisii",
    "https://www.xclusivetech.co.ke/locations/web-design-kericho",
    "https://www.xclusivetech.co.ke/locations/web-design-laikipia",
    "https://www.xclusivetech.co.ke/locations/web-design-narok",
    "https://www.xclusivetech.co.ke/locations/web-design-muranga",
    "https://www.xclusivetech.co.ke/locations/web-design-embu",
    "https://www.xclusivetech.co.ke/locations/web-design-kirinyaga",
    "https://www.xclusivetech.co.ke/locations/web-design-kitui",
    "https://www.xclusivetech.co.ke/locations/web-design-homa-bay",
    "https://www.xclusivetech.co.ke/locations/web-design-migori",
    "https://www.xclusivetech.co.ke/locations/web-design-bungoma",
    "https://www.xclusivetech.co.ke/locations/web-design-trans-nzoia",
    "https://www.xclusivetech.co.ke/locations/web-design-garissa",
    "https://www.xclusivetech.co.ke/locations/web-design-nandi",
    "https://www.xclusivetech.co.ke/locations/web-design-baringo",
    "https://www.xclusivetech.co.ke/locations/web-design-siaya",
    "https://www.xclusivetech.co.ke/locations/web-design-busia",
    "https://www.xclusivetech.co.ke/locations/web-design-vihiga",
    "https://www.xclusivetech.co.ke/locations/web-design-nyandarua",
    "https://www.xclusivetech.co.ke/locations/web-design-makueni",
    "https://www.xclusivetech.co.ke/locations/web-design-tharaka-nithi",
    "https://www.xclusivetech.co.ke/locations/web-design-nyamira",
    "https://www.xclusivetech.co.ke/locations/web-design-bomet",
    "https://www.xclusivetech.co.ke/locations/web-design-taita-taveta",
    "https://www.xclusivetech.co.ke/locations/web-design-turkana",
    "https://www.xclusivetech.co.ke/locations/web-design-samburu",
    "https://www.xclusivetech.co.ke/locations/web-design-west-pokot",
    "https://www.xclusivetech.co.ke/locations/web-design-elgeyo-marakwet",
    "https://www.xclusivetech.co.ke/locations/web-design-isiolo",
    "https://www.xclusivetech.co.ke/locations/web-design-marsabit",
    "https://www.xclusivetech.co.ke/locations/web-design-mandera",
    "https://www.xclusivetech.co.ke/locations/web-design-wajir",
    "https://www.xclusivetech.co.ke/locations/web-design-lamu",
    "https://www.xclusivetech.co.ke/locations/web-design-tana-river"
]


def main():
    print(f"Acquiring Google Indexing OAuth Token...")
    token = get_access_token()
    print(f"Token acquired. Publishing {len(PRIORITY_URLS)} priority URLs to Google Indexing API...\n")

    results = []
    success_count = 0
    fail_count = 0

    for i, url in enumerate(PRIORITY_URLS, 1):
        status, res = publish_indexing_url(token, url, 'URL_UPDATED')
        if status == 200:
            success_count += 1
            notify_time = res.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('notifyTime', 'N/A')
            print(f"[{i:02d}/{len(PRIORITY_URLS)}] 200 OK: {url} (Notified: {notify_time})")
            results.append({'url': url, 'status': 200, 'notifyTime': notify_time})
        else:
            fail_count += 1
            print(f"[{i:02d}/{len(PRIORITY_URLS)}] {status} FAILED: {url} -> {res}")
            results.append({'url': url, 'status': status, 'error': res})
        
        # Friendly rate limiting
        time.sleep(0.35)

    print(f"\n==========================================")
    print(f"Batch Publishing Complete!")
    print(f"Success: {success_count}/{len(PRIORITY_URLS)}")
    print(f"Failed:  {fail_count}/{len(PRIORITY_URLS)}")
    print(f"==========================================")

    # Save publish log
    log_path = os.path.join(os.path.dirname(__file__), '../assets/data/indexing_api_publish_log.json')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Log saved to: {log_path}")


if __name__ == '__main__':
    main()
