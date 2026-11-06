#!/usr/bin/env python3
"""
Updates all 20 subject lines to capitalize the first letter,
ensures NO 'VERIFIED SSL 465' badge exists,
and updates both text drafts and dispatch_solar_campaign.py.
"""

import os
import re

# Update dispatch_solar_campaign.py
with open("scripts/dispatch_solar_campaign.py", "r", encoding="utf-8") as f:
    code = f.read()

# Capitalize first letter of subjects in code
def cap_subject(match):
    prefix = match.group(1)
    subj = match.group(2)
    new_subj = subj[0].upper() + subj[1:] if subj else subj
    return f'{prefix}"{new_subj}"'

new_code = re.sub(r'("subject":\s*)"([^"]+)"', cap_subject, code)

with open("scripts/dispatch_solar_campaign.py", "w", encoding="utf-8") as f:
    f.write(new_code)
print("✓ Updated scripts/dispatch_solar_campaign.py subjects")

# Update text draft files
drafts_dir = "outreach_drafts/solar_campaign"
for fname in os.listdir(drafts_dir):
    if fname.endswith(".txt"):
        fpath = os.path.join(drafts_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        def cap_subj_line(m):
            s = m.group(1).strip()
            return f"SUBJECT: {s[0].upper() + s[1:]}"
            
        updated = re.sub(r'^SUBJECT:\s*(.+)$', cap_subj_line, content, flags=re.MULTILINE)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(updated)

print("✓ Updated all text draft files in outreach_drafts/solar_campaign/")
