#!/usr/bin/env python3
"""
Generate 50 Tailored Healthcare & Clinic Outreach Drafts across Kenya
Includes full-width Elite Designs branding, curiosity subject lines, 
tailored AI add-on recommendations, and Dr. Samuel Kidemi's installed signature.
"""

import json
import os

TEMPLATE_DIR = "outreach_drafts/healthcare_campaign/drafts"
DATA_FILE = "outreach_drafts/healthcare_campaign/target_50_healthcare_kenya.json"

os.makedirs(TEMPLATE_DIR, exist_ok=True)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    targets = json.load(f)

def render_html_email(item):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{item['subject']}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');
    body, table, td, p, a, li, blockquote {{
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
      font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
  </style>
</head>
<body style="margin: 0; padding: 0; background-color: #F8FAFC; color: #1E293B; font-size: 15px; line-height: 1.65;">

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #F8FAFC; width: 100% !important; margin: 0; padding: 24px 12px;">
    <tr>
      <td align="center" valign="top">

        <!-- Outer Card Container -->
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 620px; background-color: #FFFFFF; border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);">
          
          <!-- Top Elite Designs Brand Bar -->
          <tr>
            <td height="6" style="background: linear-gradient(90deg, #3600DF 0%, #3600DF 65%, #F22732 100%); line-height: 6px; font-size: 1px;">&nbsp;</td>
          </tr>

          <!-- Header with Logo -->
          <tr>
            <td style="padding: 24px 32px 18px 32px; border-bottom: 1px solid #F1F5F9; background-color: #FFFFFF;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle">
                    <a href="https://elitedesigns.co.ke" target="_blank" style="text-decoration: none; display: inline-block;">
                      <img src="https://elitedesigns.co.ke/logo.png" alt="Elite Designs Kenya" width="125" height="auto" style="display: block; border: 0; max-width: 125px; height: auto;" />
                    </a>
                  </td>
                  <td align="right" valign="middle">
                    <span style="font-size: 11px; font-weight: 700; color: #3600DF; text-transform: uppercase; letter-spacing: 0.6px; background-color: #EEF2FF; padding: 5px 10px; border-radius: 4px; border: 1px solid #C7D2FE;">
                      Executive Medical Brief
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Email Main Body Content -->
          <tr>
            <td style="padding: 32px 32px 28px 32px;">
              
              <p style="margin-top: 0; margin-bottom: 16px; font-size: 15px; color: #0F172A;">
                Dear <strong>{item['company']} Team</strong>,
              </p>

              <p style="margin-top: 0; margin-bottom: 16px; font-size: 14.5px; color: #334155; line-height: 1.65;">
                I was reviewing prominent healthcare and specialized clinical practices in <strong>{item['location']}</strong> and {item['hook']}.
              </p>

              <p style="margin-top: 0; margin-bottom: 16px; font-size: 14.5px; color: #334155; line-height: 1.65;">
                With patient expectations shifting toward rapid mobile access—especially surrounding the recent SHA/insurance transitions and after-hours appointment scheduling—I noticed an immediate opportunity to equip {item['company']} with {item['pitch_focus']}.
              </p>

              <!-- Specific Feature Highlight Box -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 20px 0; background-color: #F8FAFC; border-left: 4px solid #3600DF; border-radius: 0 8px 8px 0; padding: 14px 18px;">
                <tr>
                  <td>
                    <div style="font-size: 12px; font-weight: 700; color: #3600DF; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
                      Recommended Clinical Modernization
                    </div>
                    <div style="font-size: 13.5px; color: #1E293B; line-height: 1.55;">
                      {item['ai_feature']}
                    </div>
                  </td>
                </tr>
              </table>

              <p style="margin-top: 0; margin-bottom: 18px; font-size: 14.5px; color: #334155; line-height: 1.65;">
                Our studio, <strong>Elite Designs Kenya</strong> (operating alongside <strong>Xclusive Tech</strong>), recently delivered digital health ecosystems including the <em>GLUK School of Dentistry Portal</em>, <em>Oncolink Cancer Information Network</em>, and the <em>PataMaps Accessible Healthcare Directory</em>. We build clinical platforms engineered for sub-1-second mobile speed on Safaricom networks, paperless intake, and automated patient recall.
              </p>

              <!-- Interactive Demo Callout Box -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 24px 0 20px 0; background-color: #EEF2FF; border: 1px solid #C7D2FE; border-radius: 8px; text-align: center;">
                <tr>
                  <td style="padding: 22px 20px;">
                    <div style="font-size: 15px; font-weight: 700; color: #1E1B4B; margin-bottom: 6px;">
                      Interactive Clinical Demo Ready for {item['company']}
                    </div>
                    <div style="font-size: 13px; color: #4338CA; margin-bottom: 16px; line-height: 1.5;">
                      I have put together an interactive mobile preview showing how your practice can capture after-hours inquiries, automate patient triage, and eliminate front-desk phone bottlenecks.
                    </div>
                    <div>
                      <a href="https://wa.me/254722753819?text=Hi%20Dr.%20Samuel,%20I%20saw%20your%20brief%20regarding%20{item['company']}%20and%20would%20like%20to%20review%20the%20clinic%20interactive%20preview." target="_blank" style="display: inline-block; background-color: #3600DF; color: #FFFFFF; font-size: 13.5px; font-weight: 700; text-decoration: none; padding: 12px 26px; border-radius: 6px; box-shadow: 0 4px 12px rgba(54, 0, 223, 0.3);">
                        Review Clinic Preview on WhatsApp &rarr;
                      </a>
                    </div>
                  </td>
                </tr>
              </table>

              <p style="margin-top: 18px; margin-bottom: 24px; font-size: 14px; color: #475569;">
                Would your practice manager or clinical director be open to a 7-minute call or quick WhatsApp walkthrough this week to review the preview? Simply reply directly to this email or ping me on WhatsApp at <strong>+254 722 753 819</strong>.
              </p>

              <!-- Executive Branded Sign-off Block -->
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top: 24px; padding-top: 20px; border-top: 1px solid #E2E8F0; font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.45; color: #334155;">
                <tr>
                  <!-- Portrait Image Column -->
                  <td valign="top" style="padding-right: 16px; width: 80px; text-align: center;">
                    <a href="https://elitedesigns.co.ke" target="_blank" style="text-decoration: none; display: block;">
                      <img src="https://www.xclusivetech.co.ke/assets/images/samuel-headshot.png" alt="Dr. Samuel Kidemi" width="76" height="76" style="display: block; width: 76px; height: 76px; min-width: 76px; border-radius: 50%; border: 2px solid #3600DF; object-fit: cover;" />
                    </a>
                    <div style="margin-top: 6px;">
                      <a href="https://elitedesigns.co.ke" target="_blank" style="text-decoration: none; display: inline-block;">
                        <img src="https://elitedesigns.co.ke/logo.png" alt="Elite Designs" width="65" height="auto" style="display: block; width: 65px; max-width: 65px; height: auto;" />
                      </a>
                    </div>
                  </td>

                  <!-- Vertical Brand Gradient Divider -->
                  <td valign="top" style="width: 2px; background: linear-gradient(180deg, #3600DF 0%, #F22732 100%);">
                    <div style="width: 2px; height: 100%; min-height: 110px; font-size: 1px; line-height: 1px;">&nbsp;</div>
                  </td>

                  <!-- Information Column -->
                  <td valign="top" style="padding-left: 16px;">
                    <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td style="padding-bottom: 2px;">
                          <span style="font-size: 15px; font-weight: 800; color: #0F172A; letter-spacing: -0.2px;">Dr. Samuel Kidemi</span>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding-bottom: 6px;">
                          <span style="font-size: 11.5px; font-weight: 700; color: #3600DF; text-transform: uppercase; letter-spacing: 0.5px;">Managing Director</span>
                          <span style="color: #CBD5E1; margin: 0 4px;">&bull;</span>
                          <span style="font-size: 12px; font-weight: 600; color: #475569;">Elite Designs Kenya &amp; Xclusive Tech</span>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding-bottom: 3px; font-size: 12px; color: #475569;">
                          <span style="display: inline-block; width: 14px; color: #F22732; font-weight: bold;">&#9742;</span>
                          <strong style="color: #0F172A;">Direct / WhatsApp:</strong> 
                          <a href="https://wa.me/254722753819" target="_blank" style="color: #3600DF; text-decoration: none; font-weight: 600;">+254 722 753 819</a>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding-bottom: 3px; font-size: 12px; color: #475569;">
                          <span style="display: inline-block; width: 14px; color: #3600DF; font-weight: bold;">&#9993;</span>
                          <strong style="color: #0F172A;">Email:</strong> 
                          <a href="mailto:sam@elitedesigns.co.ke" style="color: #3600DF; text-decoration: none;">sam@elitedesigns.co.ke</a>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding-bottom: 3px; font-size: 11.5px; color: #64748B;">
                          <span style="display: inline-block; width: 14px;">&#128205;</span>
                          <span>Suite F8, Wood Ave Park Apartments, Kilimani, Nairobi</span>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding-bottom: 6px; font-size: 12px; color: #475569;">
                          <span style="display: inline-block; width: 14px; color: #3600DF;">&#127760;</span>
                          <a href="https://elitedesigns.co.ke" target="_blank" style="color: #3600DF; text-decoration: none; font-weight: 600;">elitedesigns.co.ke</a>
                          <span style="color: #CBD5E1; margin: 0 4px;">&bull;</span>
                          <a href="https://www.xclusivetech.co.ke" target="_blank" style="color: #3600DF; text-decoration: none; font-weight: 600;">xclusivetech.co.ke</a>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding-top: 2px;">
                          <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px;">
                            <tr>
                              <td style="padding: 2px 8px; font-size: 10.5px; color: #64748B; font-weight: 500;">
                                <span style="color: #D97706; font-weight: bold;">&#9733;</span> Top Digitally Fit Web Firm of the Year &bull; 120+ Sites Delivered
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

            </td>
          </tr>

          <!-- Bottom Dual Brand Bar -->
          <tr>
            <td height="5" style="background: linear-gradient(90deg, #3600DF 0%, #3600DF 70%, #F22732 100%); line-height: 5px; font-size: 1px;">&nbsp;</td>
          </tr>

        </table>

        <!-- Micro Footer -->
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 620px; margin-top: 12px;">
          <tr>
            <td align="center" style="color: #94A3B8; font-size: 11px; line-height: 1.4;">
              &copy; 2026 Elite Designs Kenya &bull; Clinical Digital Transformation &amp; Brand Systems &bull; Nairobi, Kenya
            </td>
          </tr>
        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""

def render_plain_email(item):
    return f"""Dear {item['company']} Team,

I was reviewing prominent healthcare and specialized clinical practices in {item['location']} and {item['hook']}.

With patient expectations shifting toward rapid mobile access—especially surrounding the recent SHA/insurance transitions and after-hours appointment scheduling—I noticed an immediate opportunity to equip {item['company']} with {item['pitch_focus']}.

RECOMMENDED CLINICAL MODERNIZATION:
{item['ai_feature'].replace('<strong>', '').replace('</strong>', '')}

Our studio, Elite Designs Kenya (operating alongside Xclusive Tech), recently delivered digital health ecosystems including the GLUK School of Dentistry Portal, Oncolink Cancer Information Network, and the PataMaps Accessible Healthcare Directory. We build clinical platforms engineered for sub-1-second mobile speed on Safaricom networks, paperless intake, and automated patient recall.

I have put together an interactive mobile preview showing how your practice can capture after-hours inquiries, automate patient triage, and eliminate front-desk phone bottlenecks:
https://wa.me/254722753819?text=Hi%20Dr.%20Samuel,%20I%20saw%20your%20brief%20regarding%20{item['company']}%20and%20would%20like%20to%20review%20the%20clinic%20interactive%20preview.

Would your practice manager or clinical director be open to a 7-minute call or quick WhatsApp walkthrough this week to review the preview? Simply reply directly to this email or reach me on WhatsApp at +254 722 753 819.

Warm regards,

Dr. Samuel Kidemi
Managing Director • Elite Designs Kenya & Xclusive Tech
Direct / WhatsApp: +254 722 753 819
Email: sam@elitedesigns.co.ke
Office: Suite F8, Wood Ave Park Apartments, Kilimani, Nairobi
Web: elitedesigns.co.ke • xclusivetech.co.ke
★ Top Digitally Fit Web Firm of the Year • 120+ Sites Delivered
"""

for item in targets:
    slug = f"{item['id']}_{item['company'].replace(' ', '_').replace('/', '_').replace('&', 'and')[:30]}"
    html_file = os.path.join(TEMPLATE_DIR, f"{slug}.html")
    txt_file = os.path.join(TEMPLATE_DIR, f"{slug}.txt")
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(render_html_email(item))
        
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(render_plain_email(item))

print(f"Generated {len(targets)} HTML and text drafts in {TEMPLATE_DIR}")

