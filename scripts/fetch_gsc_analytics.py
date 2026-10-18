#!/usr/bin/env python3
import sys
import os
import json
import requests
from datetime import datetime, timedelta
from search_console import get_access_token

SITE_URL = 'sc-domain:xclusivetech.co.ke'

def query_search_analytics(token, dimensions, start_date=None, end_date=None, row_limit=100):
    if not end_date:
        end_date = datetime.utcnow().strftime('%Y-%m-%d')
    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=90)).strftime('%Y-%m-%d')

    url = f'https://searchconsole.googleapis.com/webmasters/v3/sites/{requests.utils.quote(SITE_URL, safe="")}/searchAnalytics/query'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': dimensions,
        'rowLimit': row_limit
    }

    res = requests.post(url, headers=headers, json=payload, timeout=20)
    if res.status_code != 200:
        print(f"Error {res.status_code}: {res.text}")
        return []
    return res.json().get('rows', [])

def main():
    token = get_access_token()
    print(f"=== TOP SEARCH QUERIES (Last 90 Days) ===")
    queries = query_search_analytics(token, ['query'], row_limit=50)
    if not queries:
        print("No search queries found in last 90 days.")
    else:
        print(f"{'Query':<45} | {'Clicks':<8} | {'Impressions':<12} | {'CTR':<8} | {'Position'}")
        print("-" * 90)
        for r in queries:
            q = r['keys'][0]
            clicks = r.get('clicks', 0)
            imp = r.get('impressions', 0)
            ctr = f"{r.get('ctr', 0)*100:.1f}%"
            pos = f"{r.get('position', 0):.1f}"
            print(f"{q:<45} | {clicks:<8} | {imp:<12} | {ctr:<8} | {pos}")

    print("\n=== TOP PAGES (Last 90 Days) ===")
    pages = query_search_analytics(token, ['page'], row_limit=50)
    if not pages:
        print("No page data found.")
    else:
        print(f"{'Page':<65} | {'Clicks':<8} | {'Impressions':<12} | {'CTR':<8} | {'Position'}")
        print("-" * 110)
        for r in pages:
            p = r['keys'][0]
            clicks = r.get('clicks', 0)
            imp = r.get('impressions', 0)
            ctr = f"{r.get('ctr', 0)*100:.1f}%"
            pos = f"{r.get('position', 0):.1f}"
            print(f"{p:<65} | {clicks:<8} | {imp:<12} | {ctr:<8} | {pos}")

if __name__ == '__main__':
    main()
