#!/usr/bin/env python3
"""
Elite Designs — Solar Campaign Outbound Dispatch Engine
Sends 20 high-converting, personalized HTML emails with Elite Designs branding,
embedded logo, brand colors (#3600DF Royal Indigo, #F22732 Crimson Red),
and tailored AI solar conversion features.

Usage:
  python3 scripts/dispatch_solar_campaign.py --dry-run
  python3 scripts/dispatch_solar_campaign.py --send
  python3 scripts/dispatch_solar_campaign.py --send --limit 5
"""

import os
import sys
import time
import json
import ssl
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

DRAFTS_DIR = "outreach_drafts/solar_campaign"
LOG_FILE = os.path.join(DRAFTS_DIR, "dispatch_log.json")

SMTP_HOST = "mail.elitedesigns.co.ke"
SMTP_PORT = 465
SMTP_USER = "sam@elitedesigns.co.ke"
SMTP_PASS = r"G3zjz_6a3sbOypf371SE"
SENDER_NAME = "Dr. Samuel Kidemi"

CAMPAIGN_DATA = [
    {
        "id": "01",
        "company": "Ariya Finergy",
        "to_emails": ["info@ariyafinergy.com"],
        "location": "Westlands, Nairobi",
        "subject": "Quick question regarding Kalamu House / Ariya",
        "recipient": "Ariya Finergy Leadership Team",
        "hook": "saw your commercial solar installations across Kenyan flower farms and industrial facilities",
        "pitch_focus": "a dedicated C&I solar web platform engineered specifically for factory CFOs, multi-nationals, and ESG audit teams",
        "ai_feature": "an <strong>AI Satellite Rooftop Sizer</strong> that lets factory directors drop a pin on their warehouse roof to simulate solar yields, coupled with an <strong>AI Boardroom PPA vs. CAPEX Proposal Generator</strong> that exports an executive financial feasibility PDF in 60 seconds."
    },
    {
        "id": "02",
        "company": "Spenomatic Group",
        "to_emails": ["info@spenomatic.net", "sslsolar@spenomatic.net"],
        "location": "Lower Kabete, Nairobi",
        "subject": "Quick observation regarding Spenomatic solar",
        "recipient": "Spenomatic Solar Leadership",
        "hook": "followed your industrial engineering and tea factory hybrid solar work around Thika and Nairobi",
        "pitch_focus": "a dedicated industrial solar digital platform built to demonstrate high-voltage hybrid engineering and convert corporate tender inquiries with zero mobile load lag",
        "ai_feature": "an <strong>AI Factory Load Profiler</strong> that models generator-synchronization and calculates exact diesel fuel displacement liters per shift based on boiler and machinery runtime."
    },
    {
        "id": "03",
        "company": "OFGEN Africa",
        "to_emails": ["talk2us@ofgen.africa", "info@ofgen.com"],
        "location": "Kilimani, Nairobi",
        "subject": "Question on your Diani Close setup / OFGEN",
        "recipient": "OFGEN Commercial & Project Team",
        "hook": "noticed your impressive commercial solar and microgrid expansion across East Africa backed by CFAO / Toyota Tsusho",
        "pitch_focus": "an enterprise-grade renewable infrastructure web platform engineered to reflect your institutional standing and compress corporate sales cycles",
        "ai_feature": "a live <strong>AI ESG & Carbon Offset Telemetry Showcase</strong> paired with a <strong>Gated Due-Diligence Tender Room</strong> where corporate boards and financiers can securely review bankable audit certifications and EPRA Vls-1 compliance docs."
    },
    {
        "id": "04",
        "company": "Solarcentury Africa",
        "to_emails": ["enquiries@solarcenturyafrica.com"],
        "location": "Nairobi HQ",
        "subject": "Brief note for the Solarcentury engineering team",
        "recipient": "Solarcentury Africa Project Development Team",
        "hook": "tracked your multi-megawatt utility and C&I solar PV + battery storage portfolio across the continent",
        "pitch_focus": "a high-performance utility & C&I digital authority portal designed to position your regional megawatt pipeline with sub-second responsiveness",
        "ai_feature": "an <strong>AI 3D Satellite Solar Irradiance & BESS (Battery Energy Storage) Simulation Modeler</strong> that visually presents complex multi-megawatt engineering data for institutional investors and mining/industrial clients."
    },
    {
        "id": "05",
        "company": "Knights Energy",
        "to_emails": ["info@knightsandapps.com", "info@knightsenergy.ke"],
        "location": "Karen, Nairobi",
        "subject": "Saw your work around Karen / quick note",
        "recipient": "Knights Energy Leadership",
        "hook": "noticed your pioneering dual push into commercial solar and clean e-mobility / EV charging infrastructure",
        "pitch_focus": "a next-gen Solar & Clean E-Mobility digital hub that unifies your commercial solar and EV infrastructure under one high-converting web engine",
        "ai_feature": "an interactive <strong>EV Charging Station Finder map</strong> (with live connector availability and route planning) alongside an <strong>AI Fleet Fuel-to-EV TCO Comparison Tool</strong> showing delivery and corporate fleets their exact 3-year savings."
    },
    {
        "id": "06",
        "company": "Plexus Energy",
        "to_emails": ["info@plexus-energy.co.ke"],
        "location": "Ngong Road, Nairobi",
        "subject": "Quick question on your Ngong Road projects",
        "recipient": "Plexus Energy Commercial Team",
        "hook": "came across your rooftop and ground-mounted solar installations for mid-to-large commercial properties",
        "pitch_focus": "a complete commercial solar digital platform optimized for speed, client acquisition, and automated energy audit requests",
        "ai_feature": "an <strong>AI Commercial KPLC Bill Scanner</strong> where corporate clients upload a single electricity bill and receive a multi-tier hybrid sizing breakdown, backed by a <strong>24/7 AI Virtual Solar Engineer</strong> that qualifies high-ticket site audits on WhatsApp."
    },
    {
        "id": "07",
        "company": "Firstsun Technologies",
        "to_emails": ["firstsuntechnologies@gmail.com", "info@firstsuntechnologies.co.ke"],
        "location": "Nairobi",
        "subject": "Tried opening your site earlier / quick observation",
        "recipient": "Firstsun Technologies Team",
        "hook": "came across your EPRA-approved solar engineering work across schools, homes, and commercial clients",
        "pitch_focus": "a sub-second mobile web platform built on custom architecture (scoring 95+ on Google Mobile) that eliminates ad bounce and routes verified leads directly to your engineers on WhatsApp",
        "ai_feature": "an <strong>AI KPLC Bill & Token Photo Scanner</strong> where homeowners snap a picture of their electricity bill or token SMS to receive an instant, accurate hybrid backup quote, eliminating technical sizing confusion."
    },
    {
        "id": "08",
        "company": "Sunflow Systems",
        "to_emails": ["info@sunflow.co.ke", "sales@sunflow.co.ke"],
        "location": "Nairobi",
        "subject": "Question regarding your commercial solar division",
        "recipient": "Sunflow Systems Commercial Team",
        "hook": "noticed your reputation in delivering institutional and commercial solar installations paired with long-term O&M contracts",
        "pitch_focus": "a turnkey corporate solar platform engineered to convert school boards, hospital directors, and facility managers with zero friction",
        "ai_feature": "an <strong>AI Institutional Solar Financing & School Payback Simulator</strong> alongside an <strong>Automated O&M Preventive Maintenance Scheduler</strong> for commercial building managers."
    },
    {
        "id": "09",
        "company": "EOS Solar Kenya",
        "to_emails": ["info@eos.co.ke"],
        "location": "Ngong Road, Nairobi",
        "subject": "Quick note regarding your Emerald Court team",
        "recipient": "EOS Solar Engineering Team",
        "hook": "saw your solid track record in both solar photovoltaic (PV) electrical systems and solar thermal water heating solutions",
        "pitch_focus": "a modern, lightweight clean energy website that clarifies your dual PV and thermal offerings and turns high-net-worth mobile visitors into booked site surveys",
        "ai_feature": "an <strong>AI Dual-Energy Sizing Engine</strong> that compares domestic hot water energy savings against full solar PV backup, backed by an <strong>AI WhatsApp Sales Engineer</strong> that answers client questions on battery duration 24/7."
    },
    {
        "id": "10",
        "company": "Kenya Solar Installers",
        "to_emails": ["info@kenyasolarinstallers.com", "info@kenyasolarinstallers.co.ke"],
        "location": "Muchai Drive / Eastern Bypass, Nairobi",
        "subject": "Quick check on your Ngong Road / Bypass inquiries",
        "recipient": "Kenya Solar Installers Team",
        "hook": "noticed your active presence in residential rooftop and off-grid solar across Nairobi estates",
        "pitch_focus": "an ultra-fast (sub-1 second) mobile lead engine designed to stop Google and Meta ad bleed and capture residential homeowners at the exact moment they experience a blackout",
        "ai_feature": "an <strong>AI KPLC Token SMS & Bill Scanner</strong> that extracts kilowatt-hour usage in 2 seconds and generates an instant villa backup proposal with automated WhatsApp calendar booking for physical site audits."
    },
    {
        "id": "11",
        "company": "SunCulture",
        "to_emails": ["sales@sunculture.io", "sales@sunculture.com"],
        "location": "Muthangari Drive, Nairobi",
        "subject": "Quick observation on your Muthangari Drive portal",
        "recipient": "SunCulture Commercial & Growth Team",
        "hook": "followed SunCulture's remarkable footprint in climate-smart solar water pumping and drip irrigation across Kenya",
        "pitch_focus": "a streamlined, ultra-lightweight mobile web platform optimized for low-bandwidth upcountry connections with integrated Pay-As-You-Grow deposit workflows",
        "ai_feature": "a <strong>Voice-Note AI Agronomist</strong> capable of processing farmer voice notes in Swahili or English (e.g. 'Niko na ekari nne za vitunguu Kajiado') to instantly output the exact pump model, head pressure, and solar panel requirements."
    },
    {
        "id": "12",
        "company": "SolarGen Technologies",
        "to_emails": ["sales.ke@solargentechnologies.com", "info@solargentechnologies.com"],
        "location": "Old Mombasa Road, Nairobi",
        "subject": "Question regarding your Mombasa Road depot",
        "recipient": "SolarGen Commercial & Water Team",
        "hook": "tracked your engineering work in deep-borehole solar pumping, off-grid power, and community mini-grid infrastructure",
        "pitch_focus": "a comprehensive water and solar engineering digital platform built to establish authority with agricultural enterprises, NGOs, and county water departments",
        "ai_feature": "an <strong>AI Borehole Depth & Total Dynamic Head (TDH) Pumping Calculator</strong> that maps well depth, daily water yield, and pipe friction directly into an instant equipment sizing breakdown."
    },
    {
        "id": "13",
        "company": "Lean Energy Solutions",
        "to_emails": ["sales@leansolutions.co.ke", "info@leansolutions.co.ke"],
        "location": "City Park Drive, Nairobi",
        "subject": "Quick note for your City Park Drive team",
        "recipient": "Lean Energy Solutions Leadership",
        "hook": "followed your industrial energy audit, biomass boiler, and commercial clean energy solutions across Kenyan manufacturing",
        "pitch_focus": "an industrial clean energy corporate platform engineered to match your engineering authority and capture corporate decarbonization mandates",
        "ai_feature": "an <strong>AI Steam & Boiler Fuel-Switching Financial Modeler</strong> that compares heavy fuel oil (HFO) costs against hybrid solar-thermal systems with an automated Boardroom Executive Summary PDF generator."
    },
    {
        "id": "14",
        "company": "PowerPoint Systems EA",
        "to_emails": ["info@powerpoint.co.ke", "info@powerpointsystemsltd.com"],
        "location": "Lusaka Road, Nairobi",
        "subject": "Quick question regarding your Lusaka Road branch",
        "recipient": "PowerPoint Systems Commercial Leadership",
        "hook": "recognized your long-standing two-decade reputation in solar mini-grids, Tier-1 hardware importation, and power backup solutions",
        "pitch_focus": "a modern, high-performance solar distribution and EPC platform that positions your massive inventory cleanly and converts wholesale installer inquiries automatically",
        "ai_feature": "a <strong>B2B Installer Trade Portal</strong> where certified electricians and regional installers access real-time wholesale pricing, alongside an <strong>AI Technical Spec & Firmware Download Center</strong> for Huawei, Deye, and Jinko equipment."
    },
    {
        "id": "15",
        "company": "Felicity Solar Kenya",
        "to_emails": ["info@felicitysolarke.co.ke", "info@felicitysolarkenya.com"],
        "location": "Mombasa Road, Nairobi",
        "subject": "Question on your Vision Plaza showroom",
        "recipient": "Felicity Solar Kenya Management",
        "hook": "noticed your rapid growth as a premier lithium battery and hybrid inverter supplier along Mombasa Road",
        "pitch_focus": "a professional wholesale distribution web platform with password-protected installer trade pricing and automated bulk Lipa na M-Pesa order routing",
        "ai_feature": "an <strong>AI Anti-Counterfeit Serial Number & Warranty Verifier</strong> that allows buyers and installers to confirm genuine factory authenticity instantly, plus a predictive <strong>AI Battery Health & Degradation estimator</strong>."
    },
    {
        "id": "16",
        "company": "Harmonic Systems Africa",
        "to_emails": ["info@harmonicafrica.com"],
        "location": "Riverside Drive, Nairobi",
        "subject": "Quick note regarding Riverside Drive / solar",
        "recipient": "Harmonic Systems Leadership",
        "hook": "saw your high-end renewable installations, luxury solar swimming pool heating, and commercial water heating projects",
        "pitch_focus": "a sleek, luxury-tier clean energy web platform reflecting the architectural prestige of your Riverside Drive clients and converting resort and residential inquiries",
        "ai_feature": "an <strong>AI Hotel & Hospitality Hot Water Sizing Simulator</strong> that calculates diesel/electric boiler displacement savings, paired with an interactive <strong>Luxury Heated Pool Solar Sizing engine</strong>."
    },
    {
        "id": "17",
        "company": "Go Solar Systems Kenya",
        "to_emails": ["info@gosolar.co.ke", "info@gosolarltd.com"],
        "location": "Nairobi",
        "subject": "Quick question regarding your residential setups",
        "recipient": "Go Solar Systems Management",
        "hook": "noticed your residential rooftop and hybrid backup installations across suburban estates in Nairobi and Kiambu",
        "pitch_focus": "a high-converting, sub-second mobile website designed to dominate residential search and turn blackout panic into booked site audits",
        "ai_feature": "an <strong>AI KPLC Bill Photo Scanner</strong> and <strong>WhatsApp Hybrid Duration Estimator</strong> that tells estate homeowners exactly how many hours of TV, Wi-Fi, refrigeration, and security lighting they will get during power cuts."
    },
    {
        "id": "18",
        "company": "Davis & Shirtliff",
        "to_emails": ["contactcenter@dayliff.com", "info@davisandshirtliff.com"],
        "location": "Industrial Area, Nairobi",
        "subject": "Quick observation on your Industrial Area portal",
        "recipient": "Davis & Shirtliff Solar Business Unit",
        "hook": "recognized your market-leading position across East Africa in solar pumping, water heating, and power solutions",
        "pitch_focus": "a dedicated, high-speed Solar EPC division landing portal engineered to capture commercial solar bids with zero corporate site bloat",
        "ai_feature": "an <strong>AI Smart County Branch Dispatcher</strong> that instantly identifies the prospect's county location (across your 40+ branches) and routes their solar pumping or backup sizing report directly to the local branch manager's WhatsApp."
    },
    {
        "id": "19",
        "company": "Chloride Solar",
        "to_emails": ["customerservice@chlorideexide.com", "info@chlorideexide.com"],
        "location": "Commercial Street, Nairobi",
        "subject": "Quick check regarding your Commercial Street branch",
        "recipient": "Chloride Solar Management Team",
        "hook": "acknowledged your household brand authority in solar water heating, battery backup, and clean energy across Kenya",
        "pitch_focus": "a modern, responsive solar lead engine that speeds up customer self-service and sends ready-to-buy inquiries directly to your regional branch teams",
        "ai_feature": "an <strong>AI Battery Replacement & Sizing Finder</strong> that matches client appliances to the exact deep-cycle or lithium battery needed, coupled with an <strong>Automated Annual Maintenance (AMC) booking portal</strong>."
    },
    {
        "id": "20",
        "company": "PowerGen Renewable Energy",
        "to_emails": ["info@powergen-re.com"],
        "location": "Nairobi HQ",
        "subject": "Quick question regarding your East Africa mini-grids",
        "recipient": "PowerGen Project Development & C&I Team",
        "hook": "tracked PowerGen's leadership in solar mini-grids, metro-grids, and decentralized commercial energy across Sub-Saharan Africa",
        "pitch_focus": "an enterprise-grade energy infrastructure digital portal built to showcase your regional clean energy impact with international aesthetic authority",
        "ai_feature": "an <strong>AI Community Energy Yield & Tariff Structure Modeler</strong> with an interactive <strong>Investor Due-Diligence Data Room</strong> for institutional partners, DFIs, and commercial off-takers."
    }
]

def render_html(item):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Elite Designs Kenya</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F1F4F9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
  
  <!-- 100% Full-Width Brand Accent Bar -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #3600DF;">
    <tr>
      <td height="5" style="background: linear-gradient(90deg, #F22732 0%, #3600DF 35%, #3600DF 100%); line-height: 5px; font-size: 1px;">&nbsp;</td>
    </tr>
  </table>

  <!-- Main Wrapper -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #F1F4F9; padding: 24px 12px 36px 12px;">
    <tr>
      <td align="center">
        
        <!-- Container Card -->
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

          <!-- Crimson Brand Notch -->
          <tr>
            <td height="2" style="background-color: #F22732; line-height: 2px; font-size: 1px; width: 120px;">&nbsp;</td>
          </tr>

          <!-- Body Content -->
          <tr>
            <td style="padding: 28px 28px 20px 28px; color: #1E293B; font-size: 14.5px; line-height: 1.65;">
              
              <p style="margin-top: 0; margin-bottom: 16px; font-size: 15px; font-weight: 600; color: #0F172A;">
                Hi {item['recipient']},
              </p>

              <p style="margin-top: 0; margin-bottom: 18px;">
                I was reviewing <strong>{item['company']}</strong>'s footprint in the Kenyan renewable space and {item['hook']}.
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
                For {item['company']} specifically, we have designed {item['pitch_focus']}:
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
                    <strong style="color: #F22732;">Flagship AI Conversion Engine:</strong> {item['ai_feature']}
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
                      Interactive Mobile Preview Ready for {item['company']}
                    </div>
                    <div style="font-size: 13px; color: #4338CA; margin-bottom: 16px; line-height: 1.5;">
                      I have put together a live demonstration showing how this platform converts mobile visitors and routes qualified audits directly to your team.
                    </div>
                    <div>
                      <a href="https://wa.me/254722753819?text=Hi%20Samuel,%20I%20saw%20your%20note%20regarding%20{item['company']}%20and%20would%20like%20to%20see%20the%20mobile%20preview." target="_blank" style="display: inline-block; background-color: #3600DF; color: #FFFFFF; font-size: 13.5px; font-weight: 700; text-decoration: none; padding: 12px 26px; border-radius: 6px; box-shadow: 0 4px 12px rgba(54, 0, 223, 0.3);">
                        Review Interactive Preview on WhatsApp &rarr;
                      </a>
                    </div>
                  </td>
                </tr>
              </table>

              <p style="margin-top: 18px; margin-bottom: 24px; font-size: 14px; color: #475569;">
                Would you be open to a 7-minute call or quick WhatsApp walkthrough this week to review the preview? Simply reply to this email or reach me directly on WhatsApp at <strong>+254 722 753 819</strong>.
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
              &copy; 2026 Elite Designs Kenya &bull; Commercial Brand &amp; Digital Solutions &bull; Nairobi, Kenya
            </td>
          </tr>
        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""

def render_plain(item):
    return f"""Hi {item['recipient']},

I was reviewing {item['company']}'s footprint in the Kenyan renewable space and {item['hook']}.

While looking at your digital presence on mobile, I noticed an important commercial gap: over 80% of Kenyan commercial directors, factory owners, and high-net-worth homeowners research solar contractors on mobile via Safaricom 4G/5G. Sluggish load speeds, dated layouts, and technical spec sheets cause qualified prospects to bounce before your engineering team ever receives their details.

At Elite Designs & Xclusive Tech, we engineer complete, custom Next-Gen Solar Web Platforms built specifically for Kenyan EPCs and renewable energy leaders—delivering sub-1.2s mobile speeds, full EPRA compliance authority, and built-in interactive financial conversion engines.

For {item['company']} specifically, we have designed {item['pitch_focus']}, featuring:

1. Sub-1.2s Zero-Bloat Mobile Architecture: Custom-coded for Kenyan mobile networks, scoring 95+ on Google PageSpeed with zero bloated WordPress plugins.
2. Flagship AI Conversion Engine: {item['ai_feature'].replace('<strong>', '').replace('</strong>', '')}
3. Automated WhatsApp Lead Routing: Every calculated sizing report or KPLC bill upload is formatted and dispatched directly to your sales engineers' WhatsApp within 3 seconds.
4. EPRA Tender Authority & Credibility: Clear EPRA class accreditation showcases, Tier-1 hardware warranty centers (Huawei, Deye, Jinko, Growatt), and filterable kWp project showcases.
5. Executive Brand & Tender Collateral: Branded company profile PDFs, institutional bid presentation decks, and field installation collateral tailored to win multi-million shilling corporate tenders.

I have already put together an interactive mobile preview demonstrating how this platform converts mobile visitors and routes qualified audits directly to your team.

Would you be open to a 7-minute call or quick WhatsApp walkthrough this week to review the preview? 

If so, let me know what day works best, or message me directly on WhatsApp at +254 722 753 819.

Best regards,

Dr. Samuel Kidemi
Managing Director | Elite Designs Kenya & Xclusive Tech
Phone / WhatsApp: +254 722 753 819
Email: sam@elitedesigns.co.ke
Office: Suite F8, Wood Ave Park Apartments, Kilimani, Nairobi
Web: https://elitedesigns.co.ke | https://www.xclusivetech.co.ke
"""

def main():
    parser = argparse.ArgumentParser(description="Elite Designs Solar Campaign Dispatcher")
    parser.add_argument("--send", action="store_true", help="Actually send emails via SMTP")
    parser.add_argument("--dry-run", action="store_true", help="Print summary without sending")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of emails to process")
    parser.add_argument("--delay", type=float, default=4.0, help="Seconds delay between sends (default 4.0s)")
    args = parser.parse_args()

    items = CAMPAIGN_DATA
    if args.limit > 0:
        items = items[:args.limit]

    print(f"Loaded {len(items)} campaign items.")

    if not args.send and not args.dry_run:
        print("Please specify either --send or --dry-run. Exiting.")
        sys.exit(0)

    log_entries = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                log_entries = json.load(f)
        except Exception:
            log_entries = []

    already_sent = {entry["id"] for entry in log_entries if entry.get("status") == "SENT"}

    if args.dry_run:
        print("\n=== DRY RUN MODE: HTML EMAIL PREVIEW ===")
        for item in items:
            status_tag = "[ALREADY SENT]" if item["id"] in already_sent else "[READY TO SEND]"
            print(f"\n{status_tag} [{item['id']}] {item['company']}")
            print(f"  To: {', '.join(item['to_emails'])}")
            print(f"  Subject: {item['subject']}")
            print(f"  Layout: Elite Designs Branded HTML (Logo, Indigo #3600DF, Crimson #F22732)")
        print("\nDry run completed successfully.")
        return

    # Real Sending Mode
    print(f"\n=== LIVE SENDING MODE (HTML & Plain Multipart) ===")
    print(f"Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT} as {SMTP_USER}...")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=30) as server:
        server.login(SMTP_USER, SMTP_PASS)
        print("✓ Authenticated successfully with server!\n")

        for idx, item in enumerate(items, 1):
            if item["id"] in already_sent:
                print(f"[{idx}/{len(items)}] Skipping {item['company']} (already sent).")
                continue

            html_content = render_html(item)
            plain_content = render_plain(item)

            msg = MIMEMultipart('alternative')
            msg['From'] = f"{SENDER_NAME} <{SMTP_USER}>"
            msg['To'] = ", ".join(item['to_emails'])
            msg['Subject'] = item['subject']
            msg['Reply-To'] = SMTP_USER

            msg.attach(MIMEText(plain_content, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

            print(f"[{idx}/{len(items)}] Sending HTML email to {item['company']} ({', '.join(item['to_emails'])})...")
            try:
                server.sendmail(SMTP_USER, item['to_emails'], msg.as_string())
                print(f"  ✓ Delivered: '{item['subject']}'")
                log_entry = {
                    "id": item["id"],
                    "company": item['company'],
                    "to": item['to_emails'],
                    "subject": item['subject'],
                    "sent_at": datetime.now().isoformat(),
                    "status": "SENT"
                }
                log_entries.append(log_entry)
                already_sent.add(item["id"])
            except Exception as e:
                print(f"  ✗ Failed: {e}")
                log_entry = {
                    "id": item["id"],
                    "company": item['company'],
                    "to": item['to_emails'],
                    "subject": item['subject'],
                    "sent_at": datetime.now().isoformat(),
                    "status": f"FAILED: {e}"
                }
                log_entries.append(log_entry)

            with open(LOG_FILE, "w", encoding="utf-8") as lf:
                json.dump(log_entries, lf, indent=2)

            if idx < len(items):
                time.sleep(args.delay)

    print(f"\nDispatch process completed! Summary saved to {LOG_FILE}")

if __name__ == "__main__":
    main()
