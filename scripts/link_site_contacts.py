"""Link Xclusive Tech's visible contact details without touching existing anchors or scripts."""
from html.parser import HTMLParser
from html import unescape,escape
from pathlib import Path
import re,subprocess
ROOT=Path(__file__).resolve().parents[1]
PATTERN=re.compile(r'[A-Z0-9._%+-]+@xclusivetech\.co\.ke|(?<!\d)(?:\+?254[\s.-]*|0)?722[\s.-]*753[\s.-]*819(?!\d)',re.I)
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
SKIP={'a','script','style','textarea','code','pre','option','head','title','button'}
def phone_href(context):
 words=re.findall(r'whatsapp|phone|call|tel(?:ephone)?',re.sub('<[^>]*>',' ',context)[-140:],re.I)
 return 'https://wa.me/254722753819' if words and words[-1].lower()=='whatsapp' else 'tel:+254722753819'
class Contacts(HTMLParser):
 def __init__(self,source):
  super().__init__(convert_charrefs=False);self.source=source;self.stack=[];self.edits=[];self.lines=[0]
  for m in re.finditer('\n',source):self.lines.append(m.end())
 def source_offset(self):
  line,col=self.getpos();return self.lines[line-1]+col
 def handle_starttag(self,tag,attrs):
  if tag not in VOID:self.stack.append((tag,self.source_offset()))
 def handle_startendtag(self,tag,attrs):pass
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):
  if any(t in SKIP for t,_ in self.stack):return
  at=self.source_offset()
  for m in PATTERN.finditer(data):
   contact=m.group();context=self.source[max(0,at-140):at]+data[:m.start()]
   href='mailto:'+contact if '@' in contact else phone_href(context)
   extra=' target="_blank" rel="noopener noreferrer"' if href.startswith('https:') else ''
   self.edits.append((at+m.start(),at+m.end(),f'<a href="{escape(href,quote=True)}" class="contact-inline-link"{extra}>{contact}</a>'))
 def result(self):
  out=self.source
  for a,b,value in reversed(self.edits):out=out[:a]+value+out[b:]
  return out
if __name__=='__main__':
 count=0;changed=[]
 for filename in subprocess.check_output(['git','ls-files','*.html'],cwd=ROOT,text=True).splitlines():
  if filename.startswith(('assets/','scripts/','preview/')):continue
  path=ROOT/filename;source=path.read_text()
  if not re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*xclusivetech\.co\.ke',source,re.I):continue
  source=source.replace('info@xclusivetech.co.ke','hello@xclusivetech.co.ke')
  parser=Contacts(source);parser.feed(source);updated=parser.result();count+=len(parser.edits)
  # One shared observer covers contacts rendered by form feedback after page load.
  if '/js/contact-links.js' not in updated:updated=updated.replace('</body>','<script src="/js/contact-links.js?v=20261101contacts" defer></script>\n</body>')
  updated=re.sub(r'(css/styles\.css)\?v=[^"\']+',r'\1?v=20261101contacts',updated)
  if updated!=path.read_text():path.write_text(updated);changed.append(filename)
 print(f'Linked {count} plain-text contacts; shared contact handling enabled on {len(changed)} canonical pages.')
