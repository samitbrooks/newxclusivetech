#!/usr/bin/env python3
import sys
import os
import re
import time
import json
from collections import Counter
sys.path.append('scripts')
from search_console import get_access_token, inspect_url

SITE_URL = 'sc-domain:xclusivetech.co.ke'

def get_sitemap_urls():
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        content = f.read()
    return re.findall(r'<loc>(https://[^<]+)</loc>', content)

def main():
    urls = get_sitemap_urls()
    print(f"Loaded {len(urls)} URLs from sitemap.xml\n")
    token = get_access_token()

    results = []
    verdicts = Counter()
    coverages = Counter()

    for idx, u in enumerate(urls, start=1):
        try:
            status, res = inspect_url(token, SITE_URL, u)
            if status == 200:
                idx_res = res.get('inspectionResult', {}).get('indexStatusResult', {})
                verdict = idx_res.get('verdict', 'UNKNOWN')
                cov = idx_res.get('coverageState', 'UNKNOWN')
                last_crawl = idx_res.get('lastCrawlTime')
                user_canon = idx_res.get('userCanonical')
                google_canon = idx_res.get('googleCanonical')
                verdicts[verdict] += 1
                coverages[cov] += 1
                results.append({
                    'url': u,
                    'status': status,
                    'verdict': verdict,
                    'coverage': cov,
                    'last_crawl': last_crawl,
                    'user_canon': user_canon,
                    'google_canon': google_canon
                })
                # Print non-indexed or interesting ones immediately
                if verdict != 'PASS':
                    print(f"[{idx}/{len(urls)}] ⚠️ {u} -> {verdict} ({cov})")
                else:
                    print(f"[{idx}/{len(urls)}] ✅ {u} -> INDEXED")
            else:
                verdicts[f'HTTP_{status}'] += 1
                print(f"[{idx}/{len(urls)}] ❌ {u} -> HTTP {status}")
            time.sleep(0.2)
        except Exception as e:
            print(f"[{idx}/{len(urls)}] ❌ {u} -> Error: {e}")
            time.sleep(1)

    print("\n" + "="*50)
    print("INDEXING AUDIT SUMMARY")
    print("="*50)
    print("Verdicts:")
    for v, c in verdicts.items():
        print(f"  {v}: {c}")
    print("\nCoverage States:")
    for cov, c in coverages.items():
        print(f"  {cov}: {c}")

    with open('assets/data/gsc_indexing_audit.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved detailed audit to assets/data/gsc_indexing_audit.json")

if __name__ == '__main__':
    main()
