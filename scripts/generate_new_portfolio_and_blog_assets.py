#!/usr/bin/env python3
"""
generate_new_portfolio_and_blog_assets.py
Generates optimized 800x500 portfolio cards (PNG & WebP) and 1200x630 blog case study
browser mockup covers (JPG & WebP) for the 5 new portfolio websites:
1. PataMaps (patamaps.com)
2. SAN Group Limited (sangrouplimited.com)
3. Irene Muendo Isuzu (irenemuendoisuzu.co.ke)
4. Creative Kigen (creativekigen.com)
5. Elite Designs Kenya (elitedesigns.co.ke)
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PORTFOLIO_DIR = "assets/images/portfolio"
BLOG_DIR = "assets/images/blog"

os.makedirs(PORTFOLIO_DIR, exist_ok=True)
os.makedirs(BLOG_DIR, exist_ok=True)

PROJECTS = [
    {
        "id": "patamaps",
        "domain": "patamaps.com",
        "src": "/tmp/live_patamaps.png",
        "blog_slug": "case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya",
        "crop_top": 0
    },
    {
        "id": "sangrouplimited",
        "domain": "sangrouplimited.com",
        "src": "/tmp/live_sangrouplimited.png",
        "blog_slug": "case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal",
        "crop_top": 0
    },
    {
        "id": "irenemuendoisuzu",
        "domain": "irenemuendoisuzu.co.ke",
        "src": "/tmp/live_irenemuendoisuzu.png",
        "blog_slug": "case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi",
        "crop_top": 0
    },
    {
        "id": "creativekigen",
        "domain": "creativekigen.com",
        "src": "/tmp/live_creativekigen.png",
        "blog_slug": "case-study-how-we-built-creative-kigen-design-portfolio-website",
        "crop_top": 0
    },
    {
        "id": "elitedesigns",
        "domain": "elitedesigns.co.ke",
        "src": "/tmp/live_elitedesigns.png",
        "blog_slug": "case-study-how-we-built-elite-designs-corporate-branding-website",
        "crop_top": 0
    }
]

def make_portfolio_thumb(item):
    pid = item["id"]
    src_path = item["src"]
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    
    # 16:10 aspect ratio for portfolio cards (800x500)
    target_aspect = 1.6
    target_h = int(w / target_aspect)
    if target_h <= h:
        crop = im.crop((0, 0, w, target_h))
    else:
        target_w = int(h * target_aspect)
        crop = im.crop((0, 0, target_w, h))
        
    thumb = crop.resize((800, 500), Image.Resampling.LANCZOS)
    
    png_path = os.path.join(PORTFOLIO_DIR, f"{pid}.png")
    webp_path = os.path.join(PORTFOLIO_DIR, f"{pid}.webp")
    
    thumb.save(png_path, "PNG", optimize=True)
    thumb.save(webp_path, "WEBP", quality=92)
    print(f"Generated portfolio asset: {pid} -> PNG ({os.path.getsize(png_path)} bytes), WebP ({os.path.getsize(webp_path)} bytes)")

def make_blog_mockup(item):
    slug = item["blog_slug"]
    src_path = item["src"]
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
    out_jpg = os.path.join(BLOG_DIR, f"{slug}.jpg")
    out_webp = os.path.join(BLOG_DIR, f"{slug}.webp")

    bg.save(out_jpg, "JPEG", quality=95, optimize=True)
    bg.save(out_webp, "WEBP", quality=92)

    print(f"Generated blog cover: {slug} -> JPG ({os.path.getsize(out_jpg)} bytes), WebP ({os.path.getsize(out_webp)} bytes)")

if __name__ == "__main__":
    for item in PROJECTS:
        make_portfolio_thumb(item)
        make_blog_mockup(item)
    print("\n✅ All 5 portfolio and blog visuals successfully generated!")

