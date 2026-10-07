#!/usr/bin/env python3
"""
Google Search Console Automation Tool for Xclusive Tech
Uses Google Service Account credentials to:
- List verified sites
- Submit XML sitemaps
- Retrieve sitemap crawl status
- Inspect URLs (index status, canonical verdict, crawl state)
"""

import sys
import os
import json
import time
import base64
import subprocess
import tempfile
import argparse
import requests

KEY_PATH = os.environ.get(
    'GOOGLE_SERVICE_ACCOUNT_KEY',
    '/Users/app/kenyaremotejobs-laravel/storage/app/google-indexing-key.json'
)
DEFAULT_SITE_URL = os.environ.get('GSC_SITE_URL', 'sc-domain:xclusivetech.co.ke')
DEFAULT_SITEMAP_URL = 'https://www.xclusivetech.co.ke/sitemap.xml'


def get_access_token():
    if not os.path.exists(KEY_PATH):
        raise FileNotFoundError(f"Service account key not found at: {KEY_PATH}")

    with open(KEY_PATH, 'r', encoding='utf-8') as f:
        key_data = json.load(f)

    client_email = key_data['client_email']
    private_key = key_data['private_key']

    header = base64.urlsafe_b64encode(json.dumps({'alg': 'RS256', 'typ': 'JWT'}).encode()).decode().rstrip('=')
    now = int(time.time())
    claim = base64.urlsafe_b64encode(json.dumps({
        'iss': client_email,
        'scope': 'https://www.googleapis.com/auth/webmasters https://www.googleapis.com/auth/indexing',
        'aud': 'https://oauth2.googleapis.com/token',
        'exp': now + 3600,
        'iat': now
    }).encode()).decode().rstrip('=')

    unsigned = f'{header}.{claim}'

    with tempfile.NamedTemporaryFile(mode='w', suffix='.pem') as kf:
        kf.write(private_key)
        kf.flush()
        p = subprocess.Popen(['openssl', 'dgst', '-sha256', '-sign', kf.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        sig, _ = p.communicate(input=unsigned.encode())

    jwt_token = f'{unsigned}.{base64.urlsafe_b64encode(sig).decode().rstrip("=")}'

    r = requests.post('https://oauth2.googleapis.com/token', data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': jwt_token
    }, timeout=15)

    if r.status_code != 200:
        raise RuntimeError(f"OAuth token error [{r.status_code}]: {r.text}")

    return r.json()['access_token']


def list_sites(token):
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.get('https://searchconsole.googleapis.com/webmasters/v3/sites', headers=headers, timeout=15)
    return res.json()


def submit_sitemap(token, site_url, sitemap_url):
    encoded_site = requests.utils.quote(site_url, safe='')
    encoded_sitemap = requests.utils.quote(sitemap_url, safe='')
    url = f'https://searchconsole.googleapis.com/webmasters/v3/sites/{encoded_site}/sitemaps/{encoded_sitemap}'
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.put(url, headers=headers, timeout=15)
    return res.status_code, res.text


def get_sitemaps(token, site_url):
    encoded_site = requests.utils.quote(site_url, safe='')
    url = f'https://searchconsole.googleapis.com/webmasters/v3/sites/{encoded_site}/sitemaps'
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.get(url, headers=headers, timeout=15)
    return res.json()


def inspect_url(token, site_url, inspection_url):
    url = 'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        'inspectionUrl': inspection_url,
        'siteUrl': site_url
    }
    res = requests.post(url, headers=headers, json=payload, timeout=20)
    return res.status_code, res.json()


def main():
    parser = argparse.ArgumentParser(description="Google Search Console API helper")
    parser.add_argument('action', choices=['list-sites', 'submit-sitemap', 'get-sitemaps', 'inspect-url', 'inspect-core'])
    parser.add_argument('--site-url', default=DEFAULT_SITE_URL, help="GSC Site URL (e.g. sc-domain:xclusivetech.co.ke)")
    parser.add_argument('--sitemap-url', default=DEFAULT_SITEMAP_URL, help="XML Sitemap URL")
    parser.add_argument('--url', help="URL to inspect")

    args = parser.parse_args()

    try:
        token = get_access_token()
    except Exception as e:
        print(f"Auth error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.action == 'list-sites':
        sites = list_sites(token)
        print(json.dumps(sites, indent=2))

    elif args.action == 'submit-sitemap':
        status, text = submit_sitemap(token, args.site_url, args.sitemap_url)
        if status in (200, 204):
            print(f"SUCCESS: Submitted {args.sitemap_url} to {args.site_url} (HTTP {status})")
        else:
            print(f"FAILED (HTTP {status}): {text}")

    elif args.action == 'get-sitemaps':
        sitemaps = get_sitemaps(token, args.site_url)
        print(json.dumps(sitemaps, indent=2))

    elif args.action == 'inspect-url':
        if not args.url:
            print("Error: --url is required for inspect-url action", file=sys.stderr)
            sys.exit(1)
        status, res = inspect_url(token, args.site_url, args.url)
        print(json.dumps(res, indent=2))

    elif args.action == 'inspect-core':
        core_urls = [
            'https://www.xclusivetech.co.ke/',
            'https://www.xclusivetech.co.ke/pricing',
            'https://www.xclusivetech.co.ke/about',
            'https://www.xclusivetech.co.ke/services',
            'https://www.xclusivetech.co.ke/solutions',
            'https://www.xclusivetech.co.ke/portfolio',
            'https://www.xclusivetech.co.ke/founder',
            'https://www.xclusivetech.co.ke/contact',
            'https://www.xclusivetech.co.ke/terms',
            'https://www.xclusivetech.co.ke/privacy',
            'https://www.xclusivetech.co.ke/blog/best-web-design-companies-in-kenya'
        ]
        print(f"Inspecting {len(core_urls)} core URLs for {args.site_url}...\n")
        print(f"{'URL':<45} | {'Verdict':<15} | {'Coverage State'}")
        print("-" * 100)
        for u in core_urls:
            status, res = inspect_url(token, args.site_url, u)
            if status == 200:
                idx = res.get('inspectionResult', {}).get('indexStatusResult', {})
                verdict = idx.get('verdict', 'UNKNOWN')
                cov = idx.get('coverageState', 'UNKNOWN')
                print(f"{u:<45} | {verdict:<15} | {cov}")
            else:
                err = res.get('error', {}).get('message', str(res))
                print(f"{u:<45} | {'ERROR':<15} | HTTP {status}: {err}")
            time.sleep(0.5)


if __name__ == '__main__':
    main()
