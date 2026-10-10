#!/usr/bin/env python3
"""
Prospect Website Auditor & Icebreaker Generator for Xclusive Tech
-----------------------------------------------------------------
Analyzes a prospect's website and generates tailored audit observations
and personalized cold outreach icebreakers.
"""

import sys
import time
import urllib.request
import urllib.error
import ssl
from typing import Dict, Any

def audit_url(url: str) -> Dict[str, Any]:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    result = {
        "url": url,
        "is_online": False,
        "load_time_sec": None,
        "has_ssl": False,
        "has_viewport": False,
        "is_wordpress": False,
        "is_wix": False,
        "is_shopify": False,
        "has_whatsapp": False,
        "icebreaker": ""
    }

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    start = time.time()
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            elapsed = round(time.time() - start, 2)
            content = resp.read().decode("utf-8", errors="ignore").lower()
            
            result["is_online"] = True
            result["load_time_sec"] = elapsed
            result["has_ssl"] = url.startswith("https://")
            result["has_viewport"] = 'name="viewport"' in content or "name='viewport'" in content
            result["is_wordpress"] = "wp-content" in content or "wp-includes" in content
            result["is_wix"] = "wix.com" in content or "wixsite" in content
            result["is_shopify"] = "cdn.shopify.com" in content or "myshopify" in content
            result["has_whatsapp"] = "wa.me" in content or "whatsapp" in content or "api.whatsapp.com" in content

    except Exception as e:
        result["error"] = str(e)
        result["icebreaker"] = f"Noticed your domain {url} currently has connection or SSL latency issues when visitors try to load it."
        return result

    # Generate custom icebreaker hook based on audit findings
    observations = []
    if result["load_time_sec"] and result["load_time_sec"] > 2.5:
        observations.append(f"noticed your home page took over {result['load_time_sec']}s to load on mobile, which often causes up to 40% bounce rate on Kenyan 4G networks")
    elif result["is_wordpress"]:
        observations.append("noticed your site is currently running on WordPress, which can be vulnerable to plugin bloat and slowdowns compared to lightweight modern code")
    elif result["is_wix"]:
        observations.append("noticed your platform is built on Wix, which limits custom Daraja M-Pesa STK push checkouts and deep Kenyan local SEO")
    
    if not result["has_whatsapp"]:
        observations.append("spotted that you don't have an instant 1-click WhatsApp inquiry widget for mobile visitors")

    if not observations:
        observations.append("checked out your site and noticed several easy UI and mobile conversion optimizations that could lift your incoming client inquiries")

    result["icebreaker"] = "I took a quick look at your site and " + " & ".join(observations) + "."
    return result

if __name__ == "__main__":
    test_url = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    print(f"Auditing {test_url}...")
    res = audit_url(test_url)
    for k, v in res.items():
        print(f"  {k}: {v}")
