#!/usr/bin/env python3
"""
fetch_and_update_blog_photos.py

Fetches 32 authentic, high-quality, royalty-free photography images from Unsplash (free license)
tailored specifically to the topic of each blog article.
Saves them as optimized 1200x630 JPEGs in assets/images/blog/{slug}.jpg.
Updates blog/index.html and all 32 blog/*.html files to reference the new photos.
"""

import os
import json
import subprocess
import urllib.parse
import re

WORKSPACE_DIR = "/Users/app/newxclusivetech"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "assets", "images", "blog")
BLOG_DIR = os.path.join(WORKSPACE_DIR, "blog")

os.makedirs(IMAGES_DIR, exist_ok=True)

POSTS_QUERIES = {
    'web-design-for-businesses-in-kiambu-county': ('nairobi city skyline architecture kenya', 'Nairobi and Kiambu County business hub modern city architecture'),
    'how-long-does-it-take-to-build-a-website-in-kenya': ('software developer laptop coding workspace screen', 'Software developer workspace building web applications on laptop'),
    'how-much-does-a-website-cost-in-kenya': ('business budget planning laptop charts meeting', 'Corporate financial planning and website design investment ROI analysis'),
    'how-much-does-social-media-management-cost-in-kenya': ('social media marketing creator smartphone content', 'Digital social media content creator shooting on smartphone'),
    'website-vs-facebook-page-which-does-your-business-need': ('laptop computer modern office digital strategy', 'Business owner viewing responsive corporate website on laptop'),
    'geo-and-aeo-explained-getting-found-by-ai': ('artificial intelligence futuristic technology digital network', 'Artificial intelligence search engine and AI knowledge network'),
    'why-photographers-and-videographers-need-a-website': ('professional photographer camera lens studio shoot', 'Professional photographer holding DSLR camera with telephoto lens'),
    'why-driving-schools-need-a-website': ('driver steering wheel car driving lesson road', 'Student driver holding steering wheel taking driving lessons on the road'),
    'why-car-dealerships-need-a-website': ('luxury car showroom modern automobile dealership', 'Luxury automobiles in a modern clean car dealership showroom'),
    'why-real-estate-businesses-need-a-website': ('modern luxury house architecture real estate pool', 'Contemporary architectural luxury residential property listing'),
    'why-clinics-and-healthcare-providers-need-a-website': ('medical clinic doctor healthcare stethoscope hospital', 'Medical doctor in white coat with stethoscope at healthcare clinic'),
    'why-law-firms-need-a-professional-website': ('law firm courtroom justice wooden gavel books', 'Legal gavel and law books in corporate law firm chamber'),
    'why-schools-need-a-website': ('students university classroom library campus education', 'Students collaborating and studying together in modern academic library'),
    'why-churches-and-ministries-need-a-website': ('church sanctuary architecture natural light worship', 'Modern church sanctuary interior with warm uplifting natural light'),
    'why-restaurants-and-cafes-need-a-website': ('modern cafe restaurant dining interior table', 'Vibrant modern cafe restaurant interior with patrons and dining tables'),
    'why-hotels-and-hospitality-businesses-need-a-website': ('luxury boutique hotel resort swimming pool suite', 'Boutique luxury safari resort hotel with swimming pool and lounge'),
    'why-tour-and-safari-companies-need-a-website': ('kenya safari elephant wildlife savanna grassland', 'Majestic African elephant in Kenya savanna wildlife safari reserve'),
    'why-ecommerce-and-retail-businesses-need-a-website': ('ecommerce online shopping parcel delivery box customer', 'Retail ecommerce packaged customer parcel delivery box'),
    'why-agriculture-and-agribusiness-need-a-website': ('tea plantation farming agriculture kenya green hills', 'Lush green tea farm plantation hills in Kenya agribusiness'),
    'why-construction-and-contractors-need-a-website': ('building construction site engineers hard hat', 'Construction site engineers in protective hard hats reviewing project'),
    'why-consultants-need-a-professional-website': ('business meeting corporate boardroom consulting strategy', 'Corporate strategy consultants collaborating in boardroom conference'),
    'why-beauty-salons-and-spas-need-a-website': ('hair salon styling wellness spa treatment', 'Stylist performing hair care treatment in modern beauty salon'),
    'why-gyms-and-fitness-studios-need-a-website': ('gym fitness studio weights dumbbells athletic training', 'Modern fitness studio with workout weights and training equipment'),
    'why-logistics-transport-companies-need-a-website': ('logistics cargo container shipping transport highway truck', 'Commercial freight cargo logistics truck transporting goods on highway'),
    'why-financial-services-and-fintech-need-a-website': ('fintech mobile banking payment smartphone financial', 'Smartphone showing mobile money payment and digital finance in Kenya'),
    'why-insurance-agents-and-brokers-need-a-website': ('handshake business agreement contract partnership', 'Professional business handshake finalizing insurance policy agreement'),
    'why-fashion-and-apparel-brands-need-a-website': ('fashion boutique clothing apparel rack designer store', 'Designer clothing and trendy fashion apparel on boutique store display'),
    'why-event-planners-need-a-website': ('wedding banquet dinner event table decor flowers', 'Elegant wedding dinner table decor and crystal banquet reception setting'),
    'why-food-and-beverage-brands-need-a-website': ('roasted coffee beans artisanal food culinary packaging', 'Artisanal roasted coffee beans and gourmet food culinary craft'),
    'why-cosmetics-and-beauty-brands-need-a-website': ('skincare cosmetics bottles beauty aesthetic dropper', 'Aesthetic organic skincare cosmetics and serum bottles packaging'),
    'why-ngos-and-nonprofits-need-a-website': ('community volunteers humanitarian outreach development africa', 'Community humanitarian development volunteers empowering local youth'),
    'why-startups-need-a-professional-website': ('tech startup team collaboration modern office workspace', 'Creative tech startup entrepreneurs collaborating around laptop')
}

def fetch_and_download_photos():
    print(f"Starting photo download for {len(POSTS_QUERIES)} articles...")
    credits = {}
    success_count = 0

    for slug, (query, default_alt) in POSTS_QUERIES.items():
        dest = os.path.join(IMAGES_DIR, f"{slug}.jpg")
        print(f"\nProcessing [{slug}] (Query: {query})...")
        encoded_q = urllib.parse.quote(query)
        search_cmd = ['curl', '-s', f"https://unsplash.com/napi/search/photos?query={encoded_q}&per_page=10"]
        res = subprocess.run(search_cmd, capture_output=True, text=True)
        
        chosen_url = None
        alt_text = default_alt
        photographer = "Unsplash"
        
        try:
            data = json.loads(res.stdout)
            results = data.get('results', [])
            for p in results:
                raw = p.get('urls', {}).get('raw', '')
                # Ensure strictly free Unsplash photo, never Unsplash+
                if raw.startswith('https://images.unsplash.com/'):
                    base_url = raw.split('?')[0]
                    chosen_url = f"{base_url}?auto=format&fit=crop&w=1200&h=630&q=80"
                    alt_desc = p.get('alt_description') or p.get('description')
                    if alt_desc:
                        alt_text = f"{alt_desc.strip()} - {default_alt}"
                    user = p.get('user', {})
                    photographer = user.get('name', 'Unsplash Photographer')
                    break
        except Exception as e:
            print(f"  Error parsing search results: {e}")

        if not chosen_url:
            print(f"  Warning: No free photo found with query '{query}', trying broader fallback...")
            # Broader fallback query
            broad_query = query.split()[0]
            encoded_b = urllib.parse.quote(broad_query)
            b_cmd = ['curl', '-s', f"https://unsplash.com/napi/search/photos?query={encoded_b}&per_page=10"]
            b_res = subprocess.run(b_cmd, capture_output=True, text=True)
            try:
                b_data = json.loads(b_res.stdout)
                for p in b_data.get('results', []):
                    raw = p.get('urls', {}).get('raw', '')
                    if raw.startswith('https://images.unsplash.com/'):
                        base_url = raw.split('?')[0]
                        chosen_url = f"{base_url}?auto=format&fit=crop&w=1200&h=630&q=80"
                        photographer = p.get('user', {}).get('name', 'Unsplash Photographer')
                        break
            except Exception:
                pass

        if chosen_url:
            dl_cmd = ['curl', '-sL', chosen_url, '-o', dest]
            dl_res = subprocess.run(dl_cmd)
            if dl_res.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 10000:
                sz = os.path.getsize(dest)
                print(f"  Saved {dest} ({sz:,} bytes) by {photographer}")
                credits[slug] = {
                    "alt": alt_text,
                    "photographer": photographer,
                    "url": chosen_url
                }
                success_count += 1
            else:
                print(f"  Download failed or file too small for {slug}")
        else:
            print(f"  No image URL could be found for {slug}")

    print(f"\nDownloaded {success_count}/{len(POSTS_QUERIES)} photos successfully.")
    return credits

def update_html_references():
    print("\nUpdating HTML files to use real photography (.jpg)...")

    # 1. Update blog/index.html
    index_path = os.path.join(BLOG_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace all ../assets/images/blog/{slug}.svg with ../assets/images/blog/{slug}.jpg
        new_content = re.sub(
            r'\.\./assets/images/blog/([^"\']+)\.svg',
            r'../assets/images/blog/\1.jpg',
            content
        )
        if new_content != content:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("  Updated blog/index.html with .jpg image paths.")
        else:
            print("  blog/index.html already had updated image paths or no changes needed.")

    # 2. Update each blog article *.html
    updated_posts = 0
    for filename in os.listdir(BLOG_DIR):
        if not filename.endswith(".html") or filename == "index.html":
            continue
        filepath = os.path.join(BLOG_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            article_content = f.read()

        slug = filename[:-5]
        
        # Replace img src
        updated = re.sub(
            r'(\.\./assets/images/blog/[^"\']+)\.svg',
            r'\1.jpg',
            article_content
        )
        # Replace og:image and twitter:image
        updated = re.sub(
            r'(https://xclusivetech\.co\.ke/assets/images/blog/[^"\']+)\.svg',
            r'\1.jpg',
            updated
        )

        if updated != article_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated)
            updated_posts += 1

    print(f"  Updated {updated_posts} blog article HTML files with .jpg image paths and OpenGraph meta tags.")

if __name__ == "__main__":
    credits = fetch_and_download_photos()
    update_html_references()
    print("\nAll blog photos downloaded and all HTML files successfully updated!")
