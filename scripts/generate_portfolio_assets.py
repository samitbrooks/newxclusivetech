#!/usr/bin/env python3
"""
Generate and optimize high-fidelity real UI screenshot assets (PNG & WebP, 800x500)
for portfolio items:
1. Teria CBO (teriacbo.org)
2. Kenya Remote Jobs (kenyaremotejobs.com)
3. Billan Beauty (billanbeauty.co.uk)
4. Greenhunt Energy (greenhuntenergy.co.ke)

Captures and renders real screenshots without chromium.
"""

import os
from PIL import Image

OUTPUT_DIR = "assets/images/portfolio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sources of real high-resolution screenshots
SOURCES = {
    "teriacbo": "/Users/app/.gemini/antigravity-ide/scratch/assets/screenshots/teriacbo.png",
    "kenyaremotejobs": "/Users/app/.gemini/antigravity-ide/scratch/assets/screenshots/kenyaremotejobs.png",
    "billanbeauty": "/tmp/billanbeauty_thumb.png",
    "greenhuntenergy": "/Users/app/.gemini/antigravity-ide/scratch/assets/screenshots/greenhunt_energy.jpg"
}

def process_screenshot(src_path, filename):
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    
    # Check if Safari toolbar (y=104 in retina 2x) needs cropping
    if "teriacbo" in filename or "kenyaremotejobs" in filename:
        if h > 1500 and w == 2560:
            im = im.crop((0, 104, w, h))
            w, h = im.size
    
    # Crop to 16:10 aspect ratio (800x500)
    target_aspect = 1.6
    target_h = int(w / target_aspect)
    if target_h <= h:
        crop = im.crop((0, 0, w, target_h))
    else:
        target_w = int(h * target_aspect)
        crop = im.crop((0, 0, target_w, h))
        
    thumb = crop.resize((800, 500), Image.Resampling.LANCZOS)
    
    png_path = os.path.join(OUTPUT_DIR, f"{filename}.png")
    webp_path = os.path.join(OUTPUT_DIR, f"{filename}.webp")
    
    thumb.save(png_path, "PNG", optimize=True)
    thumb.save(webp_path, "WEBP", quality=90)
    print(f"Generated real screenshot for {filename}: PNG ({os.path.getsize(png_path)} bytes), WebP ({os.path.getsize(webp_path)} bytes)")

if __name__ == "__main__":
    for name, path in SOURCES.items():
        if os.path.exists(path):
            process_screenshot(path, name)
        else:
            print(f"Warning: source screenshot {path} not found for {name}")
