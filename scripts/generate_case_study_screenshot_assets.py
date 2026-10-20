#!/usr/bin/env python3
"""
Generate crisp, modern, branded 1200x630 screenshot cover images (JPG & WebP)
for the 10 portfolio case study blog posts in assets/images/blog/:
1. case-study-how-i-built-opsok-medical-website-kenya
2. case-study-how-i-designed-lusweti-nabutola-law-firm-website-nairobi
3. case-study-how-i-built-sherrane-homes-real-estate-website-kenya
4. case-study-how-i-built-santorini-queen-luxury-yacht-travel-website
5. case-study-how-i-built-vape-collective-ecommerce-mpesa-kenya
6. case-study-how-i-built-diani-elite-taxi-coastal-transfers-website
7. case-study-how-i-built-gluk-school-of-dentistry-medical-portal-kenya
8. case-study-how-i-built-batteriq-automotive-battery-delivery-kenya
9. case-study-how-i-built-maluki-bespoke-luxury-tailoring-fashion-website
10. case-study-how-i-built-charities-association-kenya-ngo-portal

Renders real screenshots in an elegant browser frame without chromium.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "assets/images/blog"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CASE_STUDIES = [
    {
        "slug": "case-study-how-i-built-opsok-medical-website-kenya",
        "screenshot": "assets/images/portfolio/opsok.png",
        "domain": "opsok.org",
        "crop_top": 16
    },
    {
        "slug": "case-study-how-i-designed-lusweti-nabutola-law-firm-website-nairobi",
        "screenshot": "assets/images/portfolio/luswetinabutola.png",
        "domain": "luswetinabutola.com",
        "crop_top": 0
    },
    {
        "slug": "case-study-how-i-built-sherrane-homes-real-estate-website-kenya",
        "screenshot": "assets/images/portfolio/sherranehomes.png",
        "domain": "sherranehomes.co.ke",
        "crop_top": 0
    },
    {
        "slug": "case-study-how-i-built-santorini-queen-luxury-yacht-travel-website",
        "screenshot": "assets/images/portfolio/santoriniqueen.png",
        "domain": "santoriniqueen.com",
        "crop_top": 0
    },
    {
        "slug": "case-study-how-i-built-vape-collective-ecommerce-mpesa-kenya",
        "screenshot": "assets/images/portfolio/vapecollectivekenya.png",
        "domain": "vapecollectivekenya.com",
        "crop_top": 0
    },
    {
        "slug": "case-study-how-i-built-diani-elite-taxi-coastal-transfers-website",
        "screenshot": "assets/images/portfolio/dianielitetaxi.png",
        "domain": "dianielitetaxi.co.ke",
        "crop_top": 0
    },
    {
        "slug": "case-study-how-i-built-gluk-school-of-dentistry-medical-portal-kenya",
        "screenshot": "assets/images/portfolio/gluksdbs.png",
        "domain": "gluksdbs.com",
        "crop_top": 22
    },
    {
        "slug": "case-study-how-i-built-batteriq-automotive-battery-delivery-kenya",
        "screenshot": "assets/images/portfolio/batteriq.png",
        "domain": "batteriq.co.ke",
        "crop_top": 0
    },
    {
        "slug": "case-study-how-i-built-maluki-bespoke-luxury-tailoring-fashion-website",
        "screenshot": "assets/images/portfolio/malukibespoke.png",
        "domain": "malukibespoke.com",
        "crop_top": 0
    },
    {
        "slug": "case-study-how-i-built-charities-association-kenya-ngo-portal",
        "screenshot": "assets/images/portfolio/cak.png",
        "domain": "cak.or.ke",
        "crop_top": 0
    }
]

def render_screenshot_card(item):
    slug = item["slug"]
    src_path = item["screenshot"]
    domain = item["domain"]
    crop_top = item.get("crop_top", 0)

    W, H = 1200, 630

    # 1. Base Canvas with deep slate gradient
    bg = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(bg)

    for y in range(H):
        ratio = y / H
        r = int(15 + (26 - 15) * ratio)
        g = int(23 + (36 - 23) * ratio)
        b = int(42 + (55 - 42) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Open screenshot
    site_img = Image.open(src_path).convert("RGB")
    if crop_top > 0:
        site_img = site_img.crop((0, crop_top, site_img.width, site_img.height))

    # 3. Browser Window Mockup dimensions
    bw = 1060
    bh = 540
    bx = (W - bw) // 2
    by = (H - bh) // 2 + 10

    # 4. Drop Shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([(bx - 8, by - 6), (bx + bw + 8, by + bh + 16)], radius=18, fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    bg.paste(shadow, (0, 0), shadow)

    # 5. Browser Window Chrome
    draw = ImageDraw.Draw(bg)
    header_h = 42

    # Chrome background
    draw.rounded_rectangle([(bx, by), (bx + bw, by + header_h + 20)], radius=14, fill=(241, 245, 249))
    draw.rectangle([(bx, by + header_h), (bx + bw, by + header_h + 20)], fill=(241, 245, 249))

    # Traffic light dots
    dots = [
        (bx + 20, by + 21, (239, 68, 68)),
        (bx + 38, by + 21, (245, 158, 11)),
        (bx + 56, by + 21, (16, 185, 129))
    ]
    for x, y, c in dots:
        draw.ellipse([(x - 6, y - 6), (x + 6, y + 6)], fill=c)

    # URL Bar
    url_box = [(bx + 120, by + 8), (bx + bw - 120, by + 34)]
    draw.rounded_rectangle(url_box, radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)

    try:
        font_url = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
    except Exception:
        font_url = ImageFont.load_default()

    draw.text((bx + 150, by + 13), f"https://{domain}", fill=(100, 116, 139), font=font_url)
    draw.text((bx + 132, by + 13), "🔒", fill=(16, 185, 129), font=font_url)

    # 6. Fit screenshot into browser viewport
    screen_w = bw
    screen_h = bh - header_h

    sw, sh = site_img.size
    aspect_target = screen_w / screen_h
    if (sw / sh) > aspect_target:
        crop_w = int(sh * aspect_target)
        cropped = site_img.crop(((sw - crop_w) // 2, 0, (sw + crop_w) // 2, sh))
    else:
        crop_h = int(sw / aspect_target)
        cropped = site_img.crop((0, 0, sw, crop_h))

    fitted = cropped.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
    bg.paste(fitted, (bx, by + header_h))

    # 7. Subtle border outline
    draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=14, outline=(71, 85, 105), width=1)

    # 8. Save both JPG and WebP
    out_jpg = os.path.join(OUTPUT_DIR, f"{slug}.jpg")
    out_webp = os.path.join(OUTPUT_DIR, f"{slug}.webp")

    bg.save(out_jpg, "JPEG", quality=95, optimize=True)
    bg.save(out_webp, "WEBP", quality=92)

    print(f"Generated: {out_jpg} ({os.path.getsize(out_jpg)} bytes) & {out_webp} ({os.path.getsize(out_webp)} bytes)")

if __name__ == "__main__":
    for item in CASE_STUDIES:
        render_screenshot_card(item)
    print("All 10 case study screenshot assets generated successfully.")
