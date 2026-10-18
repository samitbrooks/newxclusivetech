import urllib.request, ssl, json, re

ctx = ssl._create_unverified_context()
req = urllib.request.Request('https://elitedesigns.co.ke/portfolio', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Save full html for inspection
with open('assets/data/elitedesigns_portfolio_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved HTML, length:", len(html))

# Let's search for JSON data in the Next.js script tags
pattern = r'(\[{\"id\":\"[0-9]+\".*?\}\])'
m = re.search(pattern, html)
if m:
    raw = m.group(1)
    # in Next.js self.__next_f.push it's often JSON-escaped
    # unescape standard json string escapes
    try:
        # try direct
        items = json.loads(raw)
        print("Direct parsed:", len(items))
    except Exception:
        try:
            unescaped = raw.encode().decode('unicode_escape')
            items = json.loads(unescaped)
            print("Unicode unescaped parsed:", len(items))
        except Exception as e:
            print("Failed to parse directly:", e)
            # fallback: regex each object
            obj_pattern = r'\{"id":"([^"]+)","slug":"([^"]+)","title":"([^"]+)","category":"([^"]+)","problem":"(.*?)","solution":"(.*?)","projectUrl":"([^"]+)"'
            matches = re.findall(obj_pattern, raw)
            print("Regex found items:", len(matches))
            items = []
            for item in matches:
                items.append({
                    "id": item[0],
                    "slug": item[1],
                    "title": item[2],
                    "category": item[3],
                    "problem": item[4],
                    "solution": item[5],
                    "projectUrl": item[6]
                })

    with open('assets/data/elitedesigns_portfolio.json', 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)

    for it in items:
        print(f"[{it.get('category')}] {it.get('title')} -> {it.get('projectUrl')}")
else:
    print("Pattern not matched directly, checking keywords")
