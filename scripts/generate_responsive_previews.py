#!/usr/bin/env python3
"""Create smaller real screenshots for narrow portfolio cards; preserve originals."""
from pathlib import Path
import re,subprocess
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SIZES='(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw'
names=subprocess.check_output(['git','ls-files','*.html'],cwd=ROOT).decode().splitlines()+['project-guide.html']
files=[ROOT/n for n in dict.fromkeys(names) if not n.startswith(('scripts/','assets/','preview/')) and not n.startswith('preview') and (ROOT/n).exists()]
slugs=set()
for p in files:
 slugs.update(re.findall(r'assets/images/portfolio/([a-z0-9-]+)\.webp',p.read_text()))
slugs={s for s in slugs if not s.endswith('-400')}
old_bytes=0;new_bytes=0
for slug in slugs:
 original=ROOT/f'assets/images/portfolio/{slug}.webp'
 if not original.exists():continue
 out=original.with_name(slug+'-400.webp')
 with Image.open(original) as im:
  im=im.convert('RGB');im.thumbnail((400,400));im.save(out,'WEBP',quality=82,method=6)
 old_bytes+=original.stat().st_size;new_bytes+=out.stat().st_size
for p in files:
 s=p.read_text()
 def source(m):
  prefix,slug=m[1],m[2]
  if slug not in slugs:return m[0]
  return f'<source srcset="{prefix}{slug}-400.webp 400w, {prefix}{slug}.webp 800w" sizes="{SIZES}" type="image/webp">'
 s=re.sub(r'<source srcset="((?:\.\./|/)?assets/images/portfolio/)([a-z0-9-]+)\.webp" type="image/webp">',source,s)
 def image(m):
  tag=m[0]
  if 'srcset=' in tag:return tag
  match=re.search(r'src="((?:\.\./|/)?assets/images/portfolio/)([a-z0-9-]+)\.webp"',tag)
  if not match or match[2] not in slugs:return tag
  prefix,slug=match.groups()
  return tag[:-1]+f' srcset="{prefix}{slug}-400.webp 400w, {prefix}{slug}.webp 800w" sizes="{SIZES}">'
 s=re.sub(r'<img\b[^>]*>',image,s)
 p.write_text(s)
print(f'{len(slugs)} responsive previews; source WebP bytes={old_bytes}, 400px WebP bytes={new_bytes}; reduction={100*(1-new_bytes/old_bytes):.1f}% for the smaller variants')

# The shared 120px project-lead photo should not transfer the original large PNG.
portrait=ROOT/'assets/images/samuel-headshot.png'
if portrait.exists():
 for width,suffix in [(256,'-256'),(800,'')]:
  with Image.open(portrait) as im:
   im.thumbnail((width,width));im.save(ROOT/f'assets/images/samuel-headshot{suffix}.webp','WEBP',quality=88,method=6)
 for page in files:
  source=page.read_text()
  def portrait_tag(match):
   tag=match[0]
   if 'samuel-headshot.png' not in tag:return tag
   original=re.search(r'src="([^"]*samuel-headshot)\.png"',tag)
   if not original:return tag
   prefix=original[1]
   sizes='120px' if 'width="160"' in tag else '(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw'
   tag=tag.replace(prefix+'.png',prefix+'.webp')
   return tag[:-1]+f' srcset="{prefix}-256.webp 256w, {prefix}.webp 800w" sizes="{sizes}">'
  page.write_text(re.sub(r'<img\b[^>]*>',portrait_tag,source))
 print('Created responsive WebP portraits while preserving the original PNG')
