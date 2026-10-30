#!/usr/bin/env python3
"""Capture portfolio previews. Install: pip install playwright Pillow
Run: python scripts/capture_portfolio_screenshots.py [--only slug] [--delay 5]
Uses installed Chrome, or run `playwright install chromium` first.
Failed captures leave the existing previews untouched and return a nonzero exit.
"""
import argparse
import asyncio
from io import BytesIO
from pathlib import Path
import re
from urllib.parse import urlsplit

from PIL import Image, ImageStat
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
CARD = re.compile(r'^                <(?:a|div)\b[^>]*class="[^"]*group overflow-hidden[^"]*"[^>]*>[\s\S]*?^                </(?:a|div)>', re.MULTILINE)


def projects():
    seen = set()
    for match in CARD.finditer((ROOT / 'portfolio.html').read_text()):
        link = re.search(r'href="(https?[^"]+)"', match[0])
        if not link:
            continue
        url = link[1]
        key = urlsplit(url).netloc.lower().removeprefix('www.')
        if key in seen:
            continue
        seen.add(key)
        image = re.search(r'src="assets/images/portfolio/([^"/]+)\.png"', match[0])
        yield url, image[1] if image else key.split('.')[0]


async def capture(browser, semaphore, url, slug, delay):
    async with semaphore:
        page = await browser.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=1)
        try:
            response = await page.goto(url, wait_until='load', timeout=60000)
            if response and response.status >= 400:
                raise RuntimeError(f'HTTP {response.status}')
            # Persistent analytics connections must not prevent a capture forever.
            try:
                await page.wait_for_load_state('networkidle', timeout=15000)
            except Exception:
                pass
            await page.evaluate('''async () => {
                await document.fonts.ready;
                // Trigger lazy hero images without changing the captured position.
                window.scrollTo(0, 400);
            }''')
            await page.wait_for_timeout(500)
            await page.evaluate('window.scrollTo(0, 0)')
            await page.wait_for_function('''() => Array.from(document.images).filter(img => {
                const r = img.getBoundingClientRect();
                return r.width > 40 && r.height > 40 && r.top < innerHeight && r.bottom > 0;
            }).every(img => img.complete && img.naturalWidth > 0)''', timeout=25000)
            await page.wait_for_timeout(delay * 1000)
            text = (await page.locator('body').inner_text()).lower()
            title = (await page.title()).lower()
            if any(marker in text or marker in title for marker in (
                'please wait while your request is being verified', 'verify you are human',
                'checking your browser', 'just a moment...', 'access denied',
                'couldn’t verify the security of your connection',
                "couldn't verify the security of your connection",
                'this site can’t be reached', 'this site cannot be reached',
            )):
                raise RuntimeError('Site returned a security challenge or error page')
            raw = await page.screenshot(animations='disabled', timeout=15000)
            image = Image.open(BytesIO(raw)).convert('RGB').resize((800, 500), Image.Resampling.LANCZOS)
            if max(ImageStat.Stat(image).stddev) < 5:
                raise RuntimeError('Preview is nearly blank')
            output = ROOT / 'assets/images/portfolio'
            output.mkdir(parents=True, exist_ok=True)
            for ext in ('png', 'webp'):
                temporary = output / f'{slug}.tmp.{ext}'
                image.save(temporary, optimize=True, **({'quality': 90} if ext == 'webp' else {}))
                temporary.replace(output / f'{slug}.{ext}')
            print(f'OK {slug}', flush=True)
            return True
        except Exception as error:
            print(f'FAILED {slug}: {error}', flush=True)
            return False
        finally:
            await page.close()


async def main(args):
    selected = [(url, slug) for url, slug in projects() if not args.only or slug in args.only]
    if not selected:
        raise SystemExit('No matching portfolio projects')
    async with async_playwright() as playwright:
        chrome = Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        browser = await playwright.chromium.launch(**({'executable_path': str(chrome)} if chrome.exists() else {}))
        try:
            semaphore = asyncio.Semaphore(3)
            results = await asyncio.gather(*(capture(browser, semaphore, url, slug, args.delay) for url, slug in selected))
        finally:
            await browser.close()
    print(f'{sum(results)}/{len(results)} previews captured')
    return 0 if all(results) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', nargs='+', help='Capture selected image slugs only')
    parser.add_argument('--delay', type=float, default=5, help='Extra settling time in seconds (default: 5)')
    args = parser.parse_args()
    if args.delay < 0:
        parser.error('--delay must be nonnegative')
    raise SystemExit(asyncio.run(main(args)))
