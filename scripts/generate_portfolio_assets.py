#!/usr/bin/env python3
"""
Generate high-fidelity UI preview assets (PNG & WebP, 800x500) for new portfolio items:
1. Teria CBO (teriacbo.org)
2. Kenya Remote Jobs (kenyaremotejobs.co.ke)
3. Billan Beauty (billanbeauty.co.uk)
4. Greenhunt Energy (greenhuntenergy.co.ke)
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "assets/images/portfolio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_preview(domain, title, tag, accent_color, bg_gradient_start, bg_gradient_end, filename):
    w, h = 800, 500
    img = Image.new("RGB", (w, h), bg_gradient_start)
    draw = ImageDraw.Draw(img)

    # Gradient background
    r1, g1, b1 = bg_gradient_start
    r2, g2, b2 = bg_gradient_end
    for y in range(h):
        ratio = y / h
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Browser navbar mockup
    draw.rectangle([(0, 0), (w, 48)], fill=(245, 247, 250))
    draw.line([(0, 48), (w, 48)], fill=(220, 225, 232), width=1)
    # Browser dots
    draw.ellipse([(16, 18), (28, 30)], fill=(239, 68, 68))
    draw.ellipse([(36, 18), (48, 30)], fill=(245, 158, 11))
    draw.ellipse([(56, 18), (68, 30)], fill=(16, 185, 129))
    # URL bar
    draw.rounded_rectangle([(90, 10), (450, 38)], radius=6, fill=(255, 255, 255), outline=(220, 225, 232))
    
    # Hero card simulation
    draw.rounded_rectangle([(40, 75), (w - 40, h - 35)], radius=16, fill=(255, 255, 255), outline=(226, 232, 240))

    # Accent color top bar in card
    draw.rounded_rectangle([(40, 75), (w - 40, 83)], radius=4, fill=accent_color)

    # Sub-header inside card
    draw.rectangle([(65, 105), (160, 125)], fill=(240, 243, 248))
    draw.rectangle([(180, 110), (280, 122)], fill=(240, 243, 248))
    draw.rectangle([(300, 110), (380, 122)], fill=(240, 243, 248))

    # CTA Button in navbar
    draw.rounded_rectangle([(w - 180, 100), (w - 65, 132)], radius=6, fill=accent_color)

    # Hero headline bars
    draw.rounded_rectangle([(65, 170), (480, 205)], radius=6, fill=accent_color)
    draw.rounded_rectangle([(65, 218), (400, 248)], radius=6, fill=(30, 41, 59))
    draw.rounded_rectangle([(65, 260), (450, 275)], radius=4, fill=(148, 163, 184))
    draw.rounded_rectangle([(65, 285), (380, 298)], radius=4, fill=(203, 213, 225))

    # Action buttons
    draw.rounded_rectangle([(65, 330), (220, 375)], radius=8, fill=accent_color)
    draw.rounded_rectangle([(235, 330), (370, 375)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)

    # Feature preview cards on the right
    draw.rounded_rectangle([(510, 160), (w - 65, 430)], radius=12, fill=(248, 250, 252), outline=(226, 232, 240))
    draw.rounded_rectangle([(530, 185), (w - 85, 275)], radius=8, fill=(241, 245, 249))
    draw.rounded_rectangle([(530, 295), (w - 130, 312)], radius=4, fill=(51, 65, 85))
    draw.rounded_rectangle([(530, 325), (w - 85, 337)], radius=3, fill=(148, 163, 184))
    draw.rounded_rectangle([(530, 347), (w - 110, 359)], radius=3, fill=(203, 213, 225))
    draw.rounded_rectangle([(530, 380), (640, 412)], radius=6, fill=accent_color)

    # Bottom trust badge bar
    draw.rounded_rectangle([(65, 415), (460, 445)], radius=6, fill=(241, 245, 249))

    # Save PNG and WebP
    png_path = os.path.join(OUTPUT_DIR, f"{filename}.png")
    webp_path = os.path.join(OUTPUT_DIR, f"{filename}.webp")
    
    img.save(png_path, "PNG", optimize=True)
    img.save(webp_path, "WEBP", quality=90)
    print(f"Generated {png_path} and {webp_path}")

# 1. Teria CBO (Community & Grassroots NGO - Emerald & Gold)
create_preview(
    domain="teriacbo.org",
    title="Teria CBO",
    tag="Grassroots NGO & Community Empowerment",
    accent_color=(5, 150, 105),       # Emerald
    bg_gradient_start=(236, 253, 245),
    bg_gradient_end=(209, 250, 229),
    filename="teriacbo"
)

# 2. Kenya Remote Jobs (High-Traffic Job Board - Indigo & Mint)
create_preview(
    domain="kenyaremotejobs.co.ke",
    title="Kenya Remote Jobs",
    tag="Remote Work & Career Platform",
    accent_color=(79, 70, 229),       # Indigo
    bg_gradient_start=(238, 242, 255),
    bg_gradient_end=(224, 231, 255),
    filename="kenyaremotejobs"
)

# 3. Billan Beauty (International London & Nairobi Luxury Skincare - Rose & Gold)
create_preview(
    domain="billanbeauty.co.uk",
    title="Billan Beauty",
    tag="International Luxury Skincare",
    accent_color=(225, 29, 72),        # Rose/Crimson
    bg_gradient_start=(255, 241, 242),
    bg_gradient_end=(254, 205, 211),
    filename="billanbeauty"
)

# 4. Greenhunt Energy (Solar & Clean Tech - Sun Gold & Forest Green)
create_preview(
    domain="greenhuntenergy.co.ke",
    title="Greenhunt Energy",
    tag="Solar Power & Clean Energy Systems",
    accent_color=(217, 119, 6),       # Amber Gold
    bg_gradient_start=(254, 243, 199),
    bg_gradient_end=(253, 230, 138),
    filename="greenhuntenergy"
)
