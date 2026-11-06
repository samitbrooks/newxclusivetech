#!/usr/bin/env python3
"""
Test HTML Email Template with Elite Designs Branding & Logo
"""

import os
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

LOGO_PATH = "assets/images/elitedesigns_logo.png"

def generate_html_email(recipient_name, company_name, location, hook, pitch_focus, ai_feature_html):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Elite Designs Kenya</title>
  <!--[if mso]>
  <style type="text/css">
    body, table, td {{font-family: Arial, Helvetica, sans-serif !important;}}
  </style>
  <![endif]-->
</head>
<body style="margin: 0; padding: 0; background-color: #F1F4F9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;">
  
  <!-- Top 100% Full-Width Brand Accent Bar -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #3600DF;">
    <tr>
      <td height="5" style="background: linear-gradient(90deg, #F22732 0%, #3600DF 35%, #3600DF 100%); line-height: 5px; font-size: 1px;">&nbsp;</td>
    </tr>
  </table>

  <!-- Main Wrapper -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #F1F4F9; padding: 24px 12px 36px 12px;">
    <tr>
      <td align="center">
        
        <!-- Email Container Card -->
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 620px; background-color: #FFFFFF; border-radius: 10px; border: 1px solid #E2E8F0; overflow: hidden; box-shadow: 0 4px 18px rgba(54, 0, 223, 0.06);">
          
          <!-- Header Bar with Logo -->
          <tr>
            <td style="padding: 22px 28px 18px 28px; background-color: #FFFFFF; border-bottom: 1px solid #EEF2F6;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle">
                    <a href="https://elitedesigns.co.ke" target="_blank" style="text-decoration: none; display: inline-block;">
                      <img src="https://elitedesigns.co.ke/logo.png" alt="Elite Designs Kenya" width="145" height="36" style="display: block; border: 0; width: 145px; max-width: 150px; height: auto;" />
                    </a>
                  </td>
                  <td align="right" valign="middle">
                    <span style="display: inline-block; background-color: #EEF2FF; color: #3600DF; border: 1px solid #C7D2FE; font-size: 10.5px; font-weight: 700; text-transform: uppercase; padding: 4px 9px; border-radius: 4px; letter-spacing: 0.5px;">
                      CleanTech &bull; EPC Division
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Subtle Crimson Brand Accent Notch -->
          <tr>
            <td height="2" style="background-color: #F22732; line-height: 2px; font-size: 1px; width: 120px;">&nbsp;</td>
          </tr>

          <!-- Body Content -->
          <tr>
            <td style="padding: 28px 28px 20px 28px; color: #1E293B; font-size: 14.5px; line-height: 1.65;">
              
              <p style="margin-top: 0; margin-bottom: 16px; font-size: 15px; font-weight: 600; color: #0F172A;">
                Hi {recipient_name},
              </p>

              <p style="margin-top: 0; margin-bottom: 18px;">
                I was reviewing <strong>{company_name}</strong>'s footprint in the Kenyan renewable space and {hook}.
              </p>

              <!-- Commercial Gap Callout Box -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 20px 0; background-color: #F8FAFC; border-left: 4px solid #F22732; border-radius: 0 6px 6px 0; border-top: 1px solid #F1F5F9; border-right: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9;">
                <tr>
                  <td style="padding: 14px 18px; color: #334155; font-size: 13.5px; line-height: 1.6;">
                    <strong style="color: #0F172A;">Commercial Observation:</strong> Over <strong>80%</strong> of Kenyan commercial directors, factory owners, and high-net-worth homeowners research solar contractors on mobile via Safaricom 4G/5G. Sluggish load speeds, dated layouts, and technical spec sheets cause qualified prospects to bounce before your engineering team ever receives their details.
                  </td>
                </tr>
              </table>

              <p style="margin-top: 0; margin-bottom: 16px;">
                At <strong>Elite Designs &amp; Xclusive Tech</strong>, we engineer complete, custom Next-Gen Solar Web Platforms built specifically for Kenyan EPCs and renewable energy leaders—delivering sub-1.2s mobile speeds, full EPRA compliance authority, and built-in interactive financial conversion engines.
              </p>

              <p style="margin-top: 0; margin-bottom: 12px; font-weight: 700; color: #3600DF;">
                For {company_name} specifically, we have designed {pitch_focus}:
              </p>

              <!-- 5 Core Pillars List -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 22px;">
                <tr>
                  <td style="padding: 7px 0; vertical-align: top; width: 26px;">
                    <span style="display: inline-block; width: 18px; height: 18px; line-height: 18px; text-align: center; border-radius: 50%; background-color: #EEF2FF; color: #3600DF; font-size: 11px; font-weight: bold; border: 1px solid #C7D2FE;">1</span>
                  </td>
                  <td style="padding: 7px 0 7px 4px; color: #334155; font-size: 13.5px; line-height: 1.55;">
                    <strong style="color: #0F172A;">Sub-1.2s Zero-Bloat Mobile Architecture:</strong> Custom-coded for Kenyan mobile networks, scoring 95+ on Google PageSpeed with zero bloated WordPress plugins.
                  </td>
                </tr>
                <tr>
                  <td style="padding: 7px 0; vertical-align: top; width: 26px;">
                    <span style="display: inline-block; width: 18px; height: 18px; line-height: 18px; text-align: center; border-radius: 50%; background-color: #FEF2F2; color: #F22732; font-size: 11px; font-weight: bold; border: 1px solid #FECACA;">2</span>
                  </td>
                  <td style="padding: 7px 0 7px 4px; color: #334155; font-size: 13.5px; line-height: 1.55;">
                    <strong style="color: #F22732;">Flagship AI Conversion Engine:</strong> {ai_feature_html}
                  </td>
                </tr>
                <tr>
                  <td style="padding: 7px 0; vertical-align: top; width: 26px;">
                    <span style="display: inline-block; width: 18px; height: 18px; line-height: 18px; text-align: center; border-radius: 50%; background-color: #EEF2FF; color: #3600DF; font-size: 11px; font-weight: bold; border: 1px solid #C7D2FE;">3</span>
                  </td>
                  <td style="padding: 7px 0 7px 4px; color: #334155; font-size: 13.5px; line-height: 1.55;">
                    <strong style="color: #0F172A;">Automated WhatsApp Lead Routing:</strong> Every calculated sizing report or KPLC bill upload is formatted and dispatched directly to your sales engineers' WhatsApp within 3 seconds.
                  </td>
                </tr>
                <tr>
                  <td style="padding: 7px 0; vertical-align: top; width: 26px;">
                    <span style="display: inline-block; width: 18px; height: 18px; line-height: 18px; text-align: center; border-radius: 50%; background-color: #EEF2FF; color: #3600DF; font-size: 11px; font-weight: bold; border: 1px solid #C7D2FE;">4</span>
                  </td>
                  <td style="padding: 7px 0 7px 4px; color: #334155; font-size: 13.5px; line-height: 1.55;">
                    <strong style="color: #0F172A;">EPRA Tender Authority &amp; Credibility:</strong> Clear EPRA class accreditation showcases, Tier-1 hardware warranty centers (Huawei, Deye, Jinko, Growatt), and filterable kWp project showcases.
                  </td>
                </tr>
                <tr>
                  <td style="padding: 7px 0; vertical-align: top; width: 26px;">
                    <span style="display: inline-block; width: 18px; height: 18px; line-height: 18px; text-align: center; border-radius: 50%; background-color: #EEF2FF; color: #3600DF; font-size: 11px; font-weight: bold; border: 1px solid #C7D2FE;">5</span>
                  </td>
                  <td style="padding: 7px 0 7px 4px; color: #334155; font-size: 13.5px; line-height: 1.55;">
                    <strong style="color: #0F172A;">Executive Brand &amp; Tender Collateral:</strong> Branded company profile PDFs, institutional bid presentation decks, and field installation collateral tailored to win multi-million shilling corporate tenders.
                  </td>
                </tr>
              </table>

              <!-- Interactive Demo Callout Box -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 24px 0 20px 0; background-color: #EEF2FF; border: 1px solid #C7D2FE; border-radius: 8px; text-align: center;">
                <tr>
                  <td style="padding: 22px 20px;">
                    <div style="font-size: 15px; font-weight: 700; color: #1E1B4B; margin-bottom: 6px;">
                      Interactive Mobile Preview Ready for {company_name}
                    </div>
                    <div style="font-size: 13px; color: #4338CA; margin-bottom: 16px; line-height: 1.5;">
                      I have put together a live demonstration showing how this platform converts mobile visitors and routes qualified audits directly to your team.
                    </div>
                    <div>
                      <a href="https://wa.me/254722753819?text=Hi%20Samuel,%20I%20saw%20your%20note%20regarding%20{company_name}%20and%20would%20like%20to%20see%20the%20mobile%20preview." target="_blank" style="display: inline-block; background-color: #3600DF; color: #FFFFFF; font-size: 13.5px; font-weight: 700; text-decoration: none; padding: 12px 26px; border-radius: 6px; box-shadow: 0 4px 12px rgba(54, 0, 223, 0.3);">
                        Review Interactive Preview on WhatsApp &rarr;
                      </a>
                    </div>
                  </td>
                </tr>
              </table>

              <p style="margin-top: 18px; margin-bottom: 24px; font-size: 14px; color: #475569;">
                Would you be open to a 7-minute call or quick WhatsApp walkthrough this week to review the preview? Simply reply to this email or reach me directly on WhatsApp at <strong>+254 722 753 819</strong>.
              </p>

              <!-- Sign-off Block -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top: 1px solid #E2E8F0; padding-top: 18px; margin-top: 18px;">
                <tr>
                  <td valign="top" style="padding-right: 14px; width: 44px;">
                    <img src="https://elitedesigns.co.ke/logo.png" alt="ED" width="40" height="auto" style="display: block; border-radius: 4px; max-width: 40px;" />
                  </td>
                  <td valign="top" style="color: #334155; font-size: 12.5px; line-height: 1.5;">
                    <strong style="color: #0F172A; font-size: 14px;">Dr. Samuel Kidemi</strong><br/>
                    Managing Director &bull; <strong>Elite Designs Kenya</strong> &amp; Xclusive Tech<br/>
                    <span style="color: #64748B;">Direct / WhatsApp:</span> <a href="tel:+254722753819" style="color: #3600DF; text-decoration: none; font-weight: 600;">+254 722 753 819</a><br/>
                    <span style="color: #64748B;">Email:</span> <a href="mailto:sam@elitedesigns.co.ke" style="color: #3600DF; text-decoration: none;">sam@elitedesigns.co.ke</a><br/>
                    <span style="color: #64748B;">Office:</span> Suite F8, Wood Ave Park Apartments, Kilimani, Nairobi<br/>
                    <span style="color: #64748B;">Web:</span> <a href="https://elitedesigns.co.ke" style="color: #3600DF; text-decoration: none;">elitedesigns.co.ke</a> &bull; <a href="https://www.xclusivetech.co.ke" style="color: #3600DF; text-decoration: none;">xclusivetech.co.ke</a>
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
              &copy; 2026 Elite Designs Kenya &bull; Commercial Brand &amp; Digital Solutions &bull; Nairobi, Kenya
            </td>
          </tr>
        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""
    return html

# Test sending one sample to sam@elitedesigns.co.ke
print("Generating sample HTML email for Ariya Finergy...")
sample_html = generate_html_email(
    recipient_name="Ariya Finergy Leadership Team",
    company_name="Ariya Finergy",
    location="Westlands, Nairobi",
    hook="saw your commercial solar installations across Kenyan flower farms and industrial facilities",
    pitch_focus="a dedicated C&I solar web platform engineered specifically for factory CFOs, multi-nationals, and ESG audit teams",
    ai_feature_html="Integrated an <strong>AI Satellite Rooftop Sizer</strong> that lets factory directors drop a pin on their warehouse roof to simulate solar yields, coupled with an <strong>AI Boardroom PPA vs. CAPEX Proposal Generator</strong> that exports an executive financial feasibility PDF in 60 seconds."
)

host = 'mail.elitedesigns.co.ke'
port = 465
user = 'sam@elitedesigns.co.ke'
password = r'G3zjz_6a3sbOypf371SE'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

msg = MIMEMultipart('alternative')
msg['From'] = 'Samuel Kidemi <sam@elitedesigns.co.ke>'
msg['To'] = 'sam@elitedesigns.co.ke'
msg['Subject'] = 'PREVIEW: quick question regarding Kalamu House / Ariya'

# Plain text fallback
plain_text = "Hi Ariya Finergy Leadership Team,\n\nPlease view this email in an HTML-compatible client to see the complete Elite Designs interactive layout.\n\nBest regards,\nDr. Samuel Kidemi\nElite Designs Kenya"
msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))
msg.attach(MIMEText(sample_html, 'html', 'utf-8'))

with smtplib.SMTP_SSL(host, port, context=ctx, timeout=20) as server:
    server.login(user, password)
    server.sendmail(user, ['sam@elitedesigns.co.ke'], msg.as_string())
    print("✓ Successfully sent preview HTML email to sam@elitedesigns.co.ke!")
