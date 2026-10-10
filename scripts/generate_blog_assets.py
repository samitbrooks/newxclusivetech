#!/usr/bin/env python3
"""
Generate crisp, modern, branded 1200x630 JPG cover images for 5 new blog posts in assets/images/blog/:
1. web-design-for-cbos-and-community-organisations-in-kenya.jpg
2. how-to-build-a-successful-job-board-website-in-kenya.jpg
3. multi-currency-ecommerce-kenya-selling-to-the-diaspora.jpg
4. fresh-produce-and-grocery-ecommerce-in-kenya-delivery-logistics.jpg
5. ecommerce-web-design-for-solar-and-renewable-energy-companies-in-kenya.jpg
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "assets/images/blog"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_banner(category, title_line1, title_line2, subtitle, accent_color, gradient_start, gradient_end, filename):
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), gradient_start)
    draw = ImageDraw.Draw(img)

    # 1. Background gradient
    r1, g1, b1 = gradient_start
    r2, g2, b2 = gradient_end
    for y in range(h):
        ratio = y / h
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # 2. Modern subtle geometric accent grids
    for x in range(0, w, 60):
        draw.line([(x, 0), (x, h)], fill=(255, 255, 255, 25), width=1)
    for y in range(0, h, 60):
        draw.line([(0, y), (w, y)], fill=(255, 255, 255, 25), width=1)

    # 3. Soft translucent floating container card
    draw.rounded_rectangle([(80, 70), (w - 80, h - 70)], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    # Accent top stripe
    draw.rounded_rectangle([(80, 70), (w - 80, 82)], radius=6, fill=accent_color)

    # Try to load high quality font, fallback to default
    try:
        font_cat = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
        font_brand = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except Exception:
        font_cat = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_brand = ImageFont.load_default()

    # 4. Category pill badge
    draw.rounded_rectangle([(130, 120), (450, 160)], radius=20, fill=(241, 245, 249), outline=accent_color, width=2)
    draw.text((150, 128), category.upper(), fill=accent_color, font=font_cat)

    # 5. Title lines
    draw.text((130, 195), title_line1, fill=(15, 23, 42), font=font_title)
    draw.text((130, 260), title_line2, fill=(15, 23, 42), font=font_title)

    # 6. Subtitle
    draw.text((130, 345), subtitle, fill=(71, 85, 105), font=font_sub)

    # 7. Divider
    draw.line([(130, 410), (w - 130, 410)], fill=(226, 232, 240), width=2)

    # 8. Bottom bar badges
    draw.rounded_rectangle([(130, 445), (320, 495)], radius=12, fill=accent_color)
    draw.text((150, 458), "XCLUSIVE TECH", fill=(255, 255, 255), font=font_brand)

    draw.rounded_rectangle([(340, 445), (550, 495)], radius=12, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((360, 458), "2026 STRATEGY GUIDE", fill=(51, 65, 85), font=font_brand)

    draw.text((w - 380, 458), "xclusivetech.co.ke/blog", fill=(100, 116, 139), font=font_brand)

    output_path = os.path.join(OUTPUT_DIR, filename)
    img.save(output_path, "JPEG", quality=92, optimize=True)
    print(f"Generated {output_path}")

# 1. CBO Web Design
generate_banner(
    category="NGOs & Community Organisations",
    title_line1="Web Design for CBOs in Kenya:",
    title_line2="Trust, Impact & Donor Transparency",
    subtitle="Grassroots Community Portals, M-Pesa Giving & Impact Reporting",
    accent_color=(5, 150, 105),       # Emerald
    gradient_start=(236, 253, 245),
    gradient_end=(209, 250, 229),
    filename="web-design-for-cbos-and-community-organisations-in-kenya.jpg"
)

# 2. Job Board Platform
generate_banner(
    category="Recruitment & SaaS Platforms",
    title_line1="How to Build a Successful Job Board",
    title_line2="Website in Kenya (2026 Guide)",
    subtitle="Programmatic SEO, M-Pesa Subscriptions & High-Traffic Architecture",
    accent_color=(79, 70, 229),       # Indigo
    gradient_start=(238, 242, 255),
    gradient_end=(224, 231, 255),
    filename="how-to-build-a-successful-job-board-website-in-kenya.jpg"
)

# 3. Multi-Currency E-Commerce
generate_banner(
    category="Cross-Border E-Commerce",
    title_line1="Multi-Currency E-Commerce in Kenya:",
    title_line2="Selling to Diaspora & Global Buyers",
    subtitle="Dual-Hub London & Nairobi Logistics, GBP/KES Pricing & Stripe/M-Pesa",
    accent_color=(147, 51, 234),      # Purple
    gradient_start=(250, 245, 255),
    gradient_end=(243, 232, 255),
    filename="multi-currency-ecommerce-kenya-selling-to-the-diaspora.jpg"
)

# 4. Fresh Produce E-Commerce
generate_banner(
    category="Perishable Retail & Logistics",
    title_line1="Fresh Produce & Grocery E-Commerce:",
    title_line2="Delivery Logistics & Dynamic Pricing",
    subtitle="Time-Slot Delivery, Perishable Inventory, M-Pesa STK & WhatsApp Dispatch",
    accent_color=(22, 163, 74),       # Green
    gradient_start=(240, 253, 244),
    gradient_end=(220, 252, 231),
    filename="fresh-produce-and-grocery-ecommerce-in-kenya-delivery-logistics.jpg"
)

# 5. Solar & Renewable Energy E-Commerce
generate_banner(
    category="Renewable Energy E-Commerce",
    title_line1="Solar Web Design & E-Commerce in Kenya:",
    title_line2="Kilowatt Calculators & EPRA Trust",
    subtitle="High-Ticket Equipment Checkout, Milestone Payments & Solar Spec Sheets",
    accent_color=(217, 119, 6),       # Amber
    gradient_start=(254, 243, 199),
    gradient_end=(253, 230, 138),
    filename="ecommerce-web-design-for-solar-and-renewable-energy-companies-in-kenya.jpg"
)
