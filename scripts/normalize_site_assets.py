#!/usr/bin/env python3
"""Keep generated pages static, emoji-free and connected to shared assets."""
from pathlib import Path
import re

EMOJI = re.compile(r'(?:[\U0001F1E6-\U0001F1FF]{2}|[\U0001F000-\U0001FAFF\u2600-\u27BF](?:[\ufe0e\ufe0f\U0001F3FB-\U0001F3FF])?(?:\u200d[\U0001F000-\U0001FAFF\u2600-\u27BF](?:[\ufe0e\ufe0f])?)*)')
GROUPS = {
 'pin':'📍🗺', 'trophy':'🏆🎓', 'check':'✓✅', 'star':'★🌟', 'bolt':'⚡💡🔥',
 'chat':'💬😊', 'rocket':'🚀✨🎉', 'cross':'❌✂', 'flag':'🚩🇰🇪', 'alert':'⚠🛑',
 'phone':'📱📞📟', 'briefcase':'💼🏢🏗🏛', 'video':'🎬🎙', 'lock':'🔒🔑🔓🛡',
 'file':'📋📄📘📖📁', 'globe':'🌍🌐', 'chart':'📊📈📉', 'search':'🔍👀👁',
 'clock':'🕒', 'home':'🏡🏥', 'cart':'🛒', 'mail':'✉📧📥', 'heart':'❤🤝',
 'code':'💻⚙', 'truck':'🚚🚖✈⛵', 'gift':'🎁💎', 'sun':'☀🌙', 'image':'🖼📸',
 'user':'👤♿', 'bell':'🔔', 'cloud':'☁', 'ban':'🚫', 'money':'💰', 'target':'🎯'
}

def icon_for(symbol):
 for name,chars in GROUPS.items():
  if symbol in chars or symbol[0] in chars:return name
 return 'star'

def svg(symbol):
 return f'<svg class="xt-ui-icon" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/assets/icons/ui.svg#{icon_for(symbol)}"></use></svg>'

def normalize_html(source):
 # Script, styles and attributes stay plain text: never inject SVG into JSON or JS strings.
 parts=re.split(r'(<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<!--[\s\S]*?-->|<[^>]+>)',source,flags=re.I)
 for i,part in enumerate(parts):
  if part.startswith('<'):parts[i]=EMOJI.sub('',part)
  else:
   part=re.sub(r'&#(?:x([0-9a-fA-F]+)|(\d+));',lambda m: (lambda char: char if EMOJI.fullmatch(char) else m[0])(chr(int(m[1],16)) if m[1] else chr(int(m[2]))),part)
   parts[i]=EMOJI.sub(lambda m:svg(m[0]),part)
 source=''.join(parts)
 source=re.sub(r'<script\b[^>]*src="https://cdn\.tailwindcss\.com[^\"]*"[^>]*></script>', '<link rel="stylesheet" href="/css/utilities.css?v=20261030seo">',source)
 source=re.sub(r'<script>\s*(?:window\.tailwind\s*=|tailwind\.config\s*=)[\s\S]*?</script>','',source)
 source=re.sub(r'(css/styles\.css|js/animations\.js|js/navigation\.js|js/main\.js)(?:\?[^\"]*)?(?=")',r'\1?v=20261030seo',source)
 source=re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")(?:\.\./|\./)?assets/',r'\1https://www.xclusivetech.co.ke/assets/',source)
 if 'id="mobile-menu-toggle"' in source:
  source=source.replace('id="mobile-menu-toggle" class="mobile-menu-btn"','id="mobile-menu-btn" class="nav-mobile-toggle"')
  source=re.sub(r'(id="mobile-menu-btn"[^>]*>)\s*(?:<span class="hamburger-line"></span>\s*){3}',r'\1<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>',source)
  if 'id="mobile-menu"' not in source:
   menu='<div id="mobile-menu" class="nav-mobile-menu hidden"><a href="/" class="nav-mobile-link">Home</a><a href="/services" class="nav-mobile-link">Services</a><a href="/pricing" class="nav-mobile-link">Pricing</a><a href="/portfolio" class="nav-mobile-link">Portfolio</a><a href="/locations/" class="nav-mobile-link">Locations</a><a href="/blog/" class="nav-mobile-link">Blog</a><a href="/contact" class="nav-mobile-link">Contact</a></div>'
   source=source.replace('</header>',menu+'\n</header>',1)
 if 'js/animations.js' in source and 'js/lead-events.js' not in source:
  source=source.replace('</body>','    <script src="/js/lead-events.js?v=20261030seo" defer></script>\n</body>')
 if 'js/lead-events.js' in source and 'js/measurement-config.js' not in source:
  source=source.replace('<script src="/js/lead-events.js', '<script src="/js/measurement-config.js?v=20261030buyer" defer></script>\n    <script src="/js/vendor/web-vitals.iife.js?v=4.2.4" defer></script>\n    <script src="/js/buyer-tools.js?v=20261030buyer" defer></script>\n    <script src="/js/lead-events.js',1)
 source=re.sub(r'(css/styles\.css|css/utilities\.css|js/animations\.js|js/navigation\.js|js/main\.js|js/lead-events\.js)(?:\?[^\"]*)?(?=")',r'\1?v=20261030buyer',source)
 return re.sub(r'(?m)^[ \t]+$', '', source)

if __name__=='__main__':
 import subprocess
 names=subprocess.check_output(['git','ls-files','*.html']).decode().splitlines()
 if Path('project-guide.html').exists() and 'project-guide.html' not in names:names.append('project-guide.html')
 for name in names:
  if name.startswith(('scripts/', 'assets/', 'preview/')) or name in ('preview.html', 'preview_posts.html', 'preview_reels.html'):continue
  p=Path(name)
  if p.exists():
   s=p.read_text();updated=normalize_html(s)
   if updated!=s:p.write_text(updated)
