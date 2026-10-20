#!/usr/bin/env python3
"""
Updates HTML references for the 10 case study blog posts:
1. In blog/index.html, updates the card images to point to the new branded browser screenshot mockups in assets/images/blog/{slug}.webp and .jpg.
2. In each of the 10 blog posts (blog/case-study-*.html):
   - Updates og:image to https://www.xclusivetech.co.ke/assets/images/blog/{slug}.jpg
   - Updates twitter:image to https://www.xclusivetech.co.ke/assets/images/blog/{slug}.jpg
   - Updates schema.org BlogPosting image to https://www.xclusivetech.co.ke/assets/images/blog/{slug}.jpg
   - Updates the hero <picture> / <img> to use the new blog assets.
"""

import os
import re

POSTS = [
    {
        "slug": "case-study-how-i-built-opsok-medical-website-kenya",
        "portfolio_base": "opsok"
    },
    {
        "slug": "case-study-how-i-designed-lusweti-nabutola-law-firm-website-nairobi",
        "portfolio_base": "luswetinabutola"
    },
    {
        "slug": "case-study-how-i-built-sherrane-homes-real-estate-website-kenya",
        "portfolio_base": "sherranehomes"
    },
    {
        "slug": "case-study-how-i-built-santorini-queen-luxury-yacht-travel-website",
        "portfolio_base": "santoriniqueen"
    },
    {
        "slug": "case-study-how-i-built-vape-collective-ecommerce-mpesa-kenya",
        "portfolio_base": "vapecollectivekenya"
    },
    {
        "slug": "case-study-how-i-built-diani-elite-taxi-coastal-transfers-website",
        "portfolio_base": "dianielitetaxi"
    },
    {
        "slug": "case-study-how-i-built-gluk-school-of-dentistry-medical-portal-kenya",
        "portfolio_base": "gluksdbs"
    },
    {
        "slug": "case-study-how-i-built-batteriq-automotive-battery-delivery-kenya",
        "portfolio_base": "batteriq"
    },
    {
        "slug": "case-study-how-i-built-maluki-bespoke-luxury-tailoring-fashion-website",
        "portfolio_base": "malukibespoke"
    },
    {
        "slug": "case-study-how-i-built-charities-association-kenya-ngo-portal",
        "portfolio_base": "cak"
    }
]

def update_individual_posts():
    for item in POSTS:
        slug = item["slug"]
        base = item["portfolio_base"]
        filepath = f"blog/{slug}.html"
        if not os.path.isfile(filepath):
            print(f"Skipping missing file: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Update og:image
        content = re.sub(
            r'<meta property="og:image" content="https://www\.xclusivetech\.co\.ke/assets/images/portfolio/[^"]+">',
            f'<meta property="og:image" content="https://www.xclusivetech.co.ke/assets/images/blog/{slug}.jpg">',
            content
        )

        # 2. Update twitter:image
        content = re.sub(
            r'<meta name="twitter:image" content="https://www\.xclusivetech\.co\.ke/assets/images/portfolio/[^"]+">',
            f'<meta name="twitter:image" content="https://www.xclusivetech.co.ke/assets/images/blog/{slug}.jpg">',
            content
        )

        # 3. Update JSON-LD image
        content = re.sub(
            r'"https://www\.xclusivetech\.co\.ke/assets/images/portfolio/[^"]+"',
            f'"https://www.xclusivetech.co.ke/assets/images/blog/{slug}.jpg"',
            content
        )

        # 4. Update hero picture / img
        # Look for the hero picture block:
        hero_pattern = re.compile(
            r'<picture>\s*<source srcset="\.\./assets/images/portfolio/[^"]+" type="image/webp">\s*<img src="\.\./assets/images/portfolio/[^"]+" alt="([^"]+)" width="1200" height="630" class="([^"]+)" loading="eager" fetchpriority="high">\s*</picture>',
            re.DOTALL
        )

        def hero_repl(match):
            alt_text = match.group(1)
            return (
                f'<picture>\n'
                f'                    <source srcset="../assets/images/blog/{slug}.webp" type="image/webp">\n'
                f'                    <img src="../assets/images/blog/{slug}.jpg" alt="{alt_text}" width="1200" height="630" class="w-full h-auto object-cover" loading="eager" fetchpriority="high">\n'
                f'                </picture>'
            )

        new_content, count = hero_pattern.subn(hero_repl, content)
        if count == 0:
            # Fallback if class differed
            hero_pattern_fallback = re.compile(
                r'<picture>\s*<source srcset="[^"]+" type="image/webp">\s*<img src="\.\./assets/images/portfolio/[^"]+" alt="([^"]+)"[^>]*>\s*</picture>',
                re.DOTALL
            )
            def fallback_repl(match):
                alt_text = match.group(1)
                return (
                    f'<picture>\n'
                    f'                    <source srcset="../assets/images/blog/{slug}.webp" type="image/webp">\n'
                    f'                    <img src="../assets/images/blog/{slug}.jpg" alt="{alt_text}" width="1200" height="630" class="w-full h-auto object-cover" loading="eager" fetchpriority="high">\n'
                    f'                </picture>'
                )
            new_content, count = hero_pattern_fallback.subn(fallback_repl, content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Updated {filepath} (hero replacements: {count})")

def update_blog_index():
    index_path = "blog/index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    for item in POSTS:
        slug = item["slug"]
        base = item["portfolio_base"]

        # In blog/index.html, each card had:
        # <div class="w-full h-48 rounded-xl overflow-hidden mb-4 bg-slate-900 border border-slate-200">
        #     <img src="../assets/images/portfolio/opsok.png" alt="OPSOK medical society website screenshot" width="600" height="315" loading="lazy" decoding="async" class="w-full h-full object-cover object-top group-hover:scale-105 transition-transform duration-300">
        # </div>
        card_pattern = re.compile(
            rf'<div class="w-full h-48 rounded-xl overflow-hidden mb-4 bg-slate-900 border border-slate-200">\s*<img src="\.\./assets/images/portfolio/{base}\.png" alt="([^"]+)" width="600" height="315" loading="lazy" decoding="async" class="([^"]+)">\s*</div>'
        )

        def card_repl(match):
            alt_text = match.group(1)
            return (
                f'<div class="w-full h-48 rounded-xl overflow-hidden mb-4 bg-slate-900 border border-slate-200">\n'
                f'                        <picture>\n'
                f'                            <source srcset="../assets/images/blog/{slug}.webp" type="image/webp">\n'
                f'                            <img src="../assets/images/blog/{slug}.jpg" alt="{alt_text}" width="600" height="315" loading="lazy" decoding="async" onerror="this.onerror=null; this.src=\'/assets/images/blog/{slug}.jpg\';" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">\n'
                f'                        </picture>\n'
                f'                    </div>'
            )

        content, count = card_pattern.subn(card_repl, content)
        print(f"Index card updated for {slug}: {count} replacements")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("blog/index.html updated successfully.")

if __name__ == "__main__":
    update_individual_posts()
    update_blog_index()
