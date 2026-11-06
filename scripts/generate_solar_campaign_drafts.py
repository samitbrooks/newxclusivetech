#!/usr/bin/env python3
"""
Generate personalized, high-converting cold outreach email drafts for 20 Kenyan Solar Companies.
Includes:
- Catchy, intrigue-driven subject lines (peer-to-peer, curiosity-piquing).
- Full ground-up website build offer.
- Tailored operational & AI features for each specific brand.
- Clean sender identity: Samuel Kidemi, sam@elitedesigns.co.ke.
"""

import os

OUTPUT_DIR = "outreach_drafts/solar_campaign"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGETS = [
    {
        "filename": "01_Ariya_Finergy.txt",
        "company": "Ariya Finergy",
        "to_email": "info@ariyafinergy.com",
        "location": "Westlands, Nairobi",
        "subject": "quick question regarding Kalamu House / Ariya",
        "recipient": "Ariya Finergy Leadership Team",
        "hook": "saw your commercial solar installations across Kenyan flower farms and industrial facilities",
        "ai_feature": "an AI Satellite Rooftop Sizer that lets factory directors drop a pin on their warehouse roof to simulate solar yields, coupled with an AI Boardroom PPA vs. CAPEX Proposal Generator that exports an executive financial feasibility PDF in 60 seconds",
        "pitch_focus": "a dedicated C&I solar web platform engineered specifically for factory CFOs, multi-nationals, and ESG audit teams"
    },
    {
        "filename": "02_Spenomatic_Group.txt",
        "company": "Spenomatic Group",
        "to_email": "info@spenomatic.net, sslsolar@spenomatic.net",
        "location": "Lower Kabete, Nairobi",
        "subject": "quick observation regarding Spenomatic solar",
        "recipient": "Spenomatic Solar Leadership",
        "hook": "followed your industrial engineering and tea factory hybrid solar work around Thika and Nairobi",
        "ai_feature": "an AI Factory Load Profiler that models generator-synchronization and calculates exact diesel fuel displacement liters per shift based on boiler and machinery runtime",
        "pitch_focus": "a dedicated industrial solar digital platform built to demonstrate high-voltage hybrid engineering and convert corporate tender inquiries with zero mobile load lag"
    },
    {
        "filename": "03_OFGEN_Africa.txt",
        "company": "OFGEN Africa",
        "to_email": "talk2us@ofgen.africa, info@ofgen.com",
        "location": "Kilimani, Nairobi",
        "subject": "question on your Diani Close setup / OFGEN",
        "recipient": "OFGEN Commercial & Project Team",
        "hook": "noticed your impressive commercial solar and microgrid expansion across East Africa backed by CFAO / Toyota Tsusho",
        "ai_feature": "a live AI ESG & Carbon Offset Telemetry Showcase paired with a Gated Due-Diligence Tender Room where corporate boards and financiers can securely review bankable audit certifications and EPRA Vls-1 compliance docs",
        "pitch_focus": "an enterprise-grade renewable infrastructure web platform engineered to reflect your institutional standing and compress corporate sales cycles"
    },
    {
        "filename": "04_Solarcentury_Africa.txt",
        "company": "Solarcentury Africa",
        "to_email": "enquiries@solarcenturyafrica.com",
        "location": "Nairobi HQ",
        "subject": "brief note for the Solarcentury engineering team",
        "recipient": "Solarcentury Africa Project Development Team",
        "hook": "tracked your multi-megawatt utility and C&I solar PV + battery storage portfolio across the continent",
        "ai_feature": "an AI 3D Satellite Solar Irradiance & BESS (Battery Energy Storage) Simulation Modeler that visually presents complex multi-megawatt engineering data for institutional investors and mining/industrial clients",
        "pitch_focus": "a high-performance utility & C&I digital authority portal designed to position your regional megawatt pipeline with sub-second responsiveness"
    },
    {
        "filename": "05_Knights_Energy.txt",
        "company": "Knights Energy",
        "to_email": "info@knightsandapps.com, info@knightsenergy.ke",
        "location": "Karen, Nairobi",
        "subject": "saw your work around Karen / quick note",
        "recipient": "Knights Energy Leadership",
        "hook": "noticed your pioneering dual push into commercial solar and clean e-mobility / EV charging infrastructure",
        "ai_feature": "an interactive EV Charging Station Finder map (with live connector availability and route planning) alongside an AI Fleet Fuel-to-EV TCO Comparison Tool showing delivery and corporate fleets their exact 3-year savings",
        "pitch_focus": "a next-gen Solar & Clean E-Mobility digital hub that unifies your commercial solar and EV infrastructure under one high-converting web engine"
    },
    {
        "filename": "06_Plexus_Energy.txt",
        "company": "Plexus Energy",
        "to_email": "info@plexus-energy.co.ke",
        "location": "Ngong Road, Nairobi",
        "subject": "quick question on your Ngong Road projects",
        "recipient": "Plexus Energy Commercial Team",
        "hook": "came across your rooftop and ground-mounted solar installations for mid-to-large commercial properties",
        "ai_feature": "an AI Commercial KPLC Bill Scanner where corporate clients upload a single electricity bill and receive a multi-tier hybrid sizing breakdown, backed by a 24/7 AI Virtual Solar Engineer that qualifies high-ticket site audits on WhatsApp",
        "pitch_focus": "a complete commercial solar digital platform optimized for speed, client acquisition, and automated energy audit requests"
    },
    {
        "filename": "07_Firstsun_Technologies.txt",
        "company": "Firstsun Technologies",
        "to_email": "firstsuntechnologies@gmail.com, info@firstsuntechnologies.co.ke",
        "location": "Nairobi",
        "subject": "tried opening your site earlier / quick observation",
        "recipient": "Firstsun Technologies Team",
        "hook": "came across your EPRA-approved solar engineering work across schools, homes, and commercial clients",
        "ai_feature": "an AI KPLC Bill & Token Photo Scanner where homeowners snap a picture of their electricity bill or token SMS to receive an instant, accurate hybrid backup quote, eliminating technical sizing confusion",
        "pitch_focus": "a sub-second mobile web platform built on custom architecture (scoring 95+ on Google Mobile) that eliminates ad bounce and routes verified leads directly to your engineers on WhatsApp"
    },
    {
        "filename": "08_Sunflow_Systems.txt",
        "company": "Sunflow Systems",
        "to_email": "info@sunflow.co.ke, sales@sunflow.co.ke",
        "location": "Nairobi",
        "subject": "question regarding your commercial solar division",
        "recipient": "Sunflow Systems Commercial Team",
        "hook": "noticed your reputation in delivering institutional and commercial solar installations paired with long-term O&M contracts",
        "ai_feature": "an AI Institutional Solar Financing & School Payback Simulator alongside an Automated O&M Preventive Maintenance Scheduler for commercial building managers",
        "pitch_focus": "a turnkey corporate solar platform engineered to convert school boards, hospital directors, and facility managers with zero friction"
    },
    {
        "filename": "09_EOS_Solar_Kenya.txt",
        "company": "EOS Solar Kenya",
        "to_email": "info@eos.co.ke",
        "location": "Ngong Road, Nairobi",
        "subject": "quick note regarding your Emerald Court team",
        "recipient": "EOS Solar Engineering Team",
        "hook": "saw your solid track record in both solar photovoltaic (PV) electrical systems and solar thermal water heating solutions",
        "ai_feature": "an AI Dual-Energy Sizing Engine that compares domestic hot water energy savings against full solar PV backup, backed by an AI WhatsApp Sales Engineer that answers client questions on battery duration 24/7",
        "pitch_focus": "a modern, lightweight clean energy website that clarifies your dual PV and thermal offerings and turns high-net-worth mobile visitors into booked site surveys"
    },
    {
        "filename": "10_Kenya_Solar_Installers.txt",
        "company": "Kenya Solar Installers",
        "to_email": "info@kenyasolarinstallers.com, info@kenyasolarinstallers.co.ke",
        "location": "Muchai Drive / Eastern Bypass, Nairobi",
        "subject": "quick check on your Ngong Road / Bypass inquiries",
        "recipient": "Kenya Solar Installers Team",
        "hook": "noticed your active presence in residential rooftop and off-grid solar across Nairobi estates",
        "ai_feature": "an AI KPLC Token SMS & Bill Scanner that extracts kilowatt-hour usage in 2 seconds and generates an instant villa backup proposal with automated WhatsApp calendar booking for physical site audits",
        "pitch_focus": "an ultra-fast (sub-1 second) mobile lead engine designed to stop Google and Meta ad bleed and capture residential homeowners at the exact moment they experience a blackout"
    },
    {
        "filename": "11_SunCulture.txt",
        "company": "SunCulture",
        "to_email": "sales@sunculture.io, sales@sunculture.com",
        "location": "Muthangari Drive, Nairobi",
        "subject": "quick observation on your Muthangari Drive portal",
        "recipient": "SunCulture Commercial & Growth Team",
        "hook": "followed SunCulture's remarkable footprint in climate-smart solar water pumping and drip irrigation across Kenya",
        "ai_feature": "a Voice-Note AI Agronomist capable of processing farmer voice notes in Swahili or English (e.g. 'Niko na ekari nne za vitunguu Kajiado') to instantly output the exact pump model, head pressure, and solar panel requirements",
        "pitch_focus": "a streamlined, ultra-lightweight mobile web platform optimized for low-bandwidth upcountry connections with integrated Pay-As-You-Grow deposit workflows"
    },
    {
        "filename": "12_SolarGen_Technologies.txt",
        "company": "SolarGen Technologies",
        "to_email": "sales.ke@solargentechnologies.com, info@solargentechnologies.com",
        "location": "Old Mombasa Road, Nairobi",
        "subject": "question regarding your Mombasa Road depot",
        "recipient": "SolarGen Commercial & Water Team",
        "hook": "tracked your engineering work in deep-borehole solar pumping, off-grid power, and community mini-grid infrastructure",
        "ai_feature": "an AI Borehole Depth & Total Dynamic Head (TDH) Pumping Calculator that maps well depth, daily water yield, and pipe friction directly into an instant equipment sizing breakdown",
        "pitch_focus": "a comprehensive water and solar engineering digital platform built to establish authority with agricultural enterprises, NGOs, and county water departments"
    },
    {
        "filename": "13_Lean_Energy_Solutions.txt",
        "company": "Lean Energy Solutions",
        "to_email": "sales@leansolutions.co.ke, info@leansolutions.co.ke",
        "location": "City Park Drive, Nairobi",
        "subject": "quick note for your City Park Drive team",
        "recipient": "Lean Energy Solutions Leadership",
        "hook": "followed your industrial energy audit, biomass boiler, and commercial clean energy solutions across Kenyan manufacturing",
        "ai_feature": "an AI Steam & Boiler Fuel-Switching Financial Modeler that compares heavy fuel oil (HFO) costs against hybrid solar-thermal systems with an automated Boardroom Executive Summary PDF generator",
        "pitch_focus": "an industrial clean energy corporate platform engineered to match your engineering authority and capture corporate decarbonization mandates"
    },
    {
        "filename": "14_PowerPoint_Systems_EA.txt",
        "company": "PowerPoint Systems EA",
        "to_email": "info@powerpoint.co.ke, info@powerpointsystemsltd.com",
        "location": "Lusaka Road, Nairobi",
        "subject": "quick question regarding your Lusaka Road branch",
        "recipient": "PowerPoint Systems Commercial Leadership",
        "hook": "recognized your long-standing two-decade reputation in solar mini-grids, Tier-1 hardware importation, and power backup solutions",
        "ai_feature": "a B2B Installer Trade Portal where certified electricians and regional installers access real-time wholesale pricing, alongside an AI Technical Spec & Firmware Download Center for Huawei, Deye, and Jinko equipment",
        "pitch_focus": "a modern, high-performance solar distribution and EPC platform that positions your massive inventory cleanly and converts wholesale installer inquiries automatically"
    },
    {
        "filename": "15_Felicity_Solar_Kenya.txt",
        "company": "Felicity Solar Kenya",
        "to_email": "info@felicitysolarke.co.ke, info@felicitysolarkenya.com",
        "location": "Mombasa Road, Nairobi",
        "subject": "question on your Vision Plaza showroom",
        "recipient": "Felicity Solar Kenya Management",
        "hook": "noticed your rapid growth as a premier lithium battery and hybrid inverter supplier along Mombasa Road",
        "ai_feature": "an AI Anti-Counterfeit Serial Number & Warranty Verifier that allows buyers and installers to confirm genuine factory authenticity instantly, plus a predictive AI Battery Health & Degradation estimator",
        "pitch_focus": "a professional wholesale distribution web platform with password-protected installer trade pricing and automated bulk Lipa na M-Pesa order routing"
    },
    {
        "filename": "16_Harmonic_Systems_Africa.txt",
        "company": "Harmonic Systems Africa",
        "to_email": "info@harmonicafrica.com",
        "location": "Riverside Drive, Nairobi",
        "subject": "quick note regarding Riverside Drive / solar",
        "recipient": "Harmonic Systems Leadership",
        "hook": "saw your high-end renewable installations, luxury solar swimming pool heating, and commercial water heating projects",
        "ai_feature": "an AI Hotel & Hospitality Hot Water Sizing Simulator that calculates diesel/electric boiler displacement savings, paired with an interactive Luxury Heated Pool Solar Sizing engine",
        "pitch_focus": "a sleek, luxury-tier clean energy web platform reflecting the architectural prestige of your Riverside Drive clients and converting resort and residential inquiries"
    },
    {
        "filename": "17_Go_Solar_Systems_Kenya.txt",
        "company": "Go Solar Systems Kenya",
        "to_email": "info@gosolar.co.ke, info@gosolarltd.com",
        "location": "Nairobi",
        "subject": "quick question regarding your residential setups",
        "recipient": "Go Solar Systems Management",
        "hook": "noticed your residential rooftop and hybrid backup installations across suburban estates in Nairobi and Kiambu",
        "ai_feature": "an AI KPLC Bill Photo Scanner and WhatsApp Hybrid Duration Estimator that tells estate homeowners exactly how many hours of TV, Wi-Fi, refrigeration, and security lighting they will get during power cuts",
        "pitch_focus": "a high-converting, sub-second mobile website designed to dominate residential search and turn blackout panic into booked site audits"
    },
    {
        "filename": "18_Davis_and_Shirtliff.txt",
        "company": "Davis & Shirtliff",
        "to_email": "contactcenter@dayliff.com, info@davisandshirtliff.com",
        "location": "Industrial Area, Nairobi",
        "subject": "quick observation on your Industrial Area portal",
        "recipient": "Davis & Shirtliff Solar Business Unit",
        "hook": "recognized your market-leading position across East Africa in solar pumping, water heating, and power solutions",
        "ai_feature": "an AI Smart County Branch Dispatcher that instantly identifies the prospect's county location (across your 40+ branches) and routes their solar pumping or backup sizing report directly to the local branch manager's WhatsApp",
        "pitch_focus": "a dedicated, high-speed Solar EPC division landing portal engineered to capture commercial solar bids with zero corporate site bloat"
    },
    {
        "filename": "19_Chloride_Solar.txt",
        "company": "Chloride Solar (Chloride Exide)",
        "to_email": "customerservice@chlorideexide.com, info@chlorideexide.com",
        "location": "Commercial Street, Nairobi",
        "subject": "quick check regarding your Commercial Street branch",
        "recipient": "Chloride Solar Management Team",
        "hook": "acknowledged your household brand authority in solar water heating, battery backup, and clean energy across Kenya",
        "ai_feature": "an AI Battery Replacement & Sizing Finder that matches client appliances to the exact deep-cycle or lithium battery needed, coupled with an Automated Annual Maintenance (AMC) booking portal",
        "pitch_focus": "a modern, responsive solar lead engine that speeds up customer self-service and sends ready-to-buy inquiries directly to your regional branch teams"
    },
    {
        "filename": "20_PowerGen_Renewable_Energy.txt",
        "company": "PowerGen Renewable Energy",
        "to_email": "info@powergen-re.com",
        "location": "Nairobi HQ",
        "subject": "quick question regarding your East Africa mini-grids",
        "recipient": "PowerGen Project Development & C&I Team",
        "hook": "tracked PowerGen's leadership in solar mini-grids, metro-grids, and decentralized commercial energy across Sub-Saharan Africa",
        "ai_feature": "an AI Community Energy Yield & Tariff Structure Modeler with an interactive Investor Due-Diligence Data Room for institutional partners, DFIs, and commercial off-takers",
        "pitch_focus": "an enterprise-grade energy infrastructure digital portal built to showcase your regional clean energy impact with international aesthetic authority"
    }
]

def build_email_text(target):
    body = f"""TO: {target['to_email']}
SUBJECT: {target['subject']}
FROM: Samuel Kidemi <sam@elitedesigns.co.ke>
COMPANY: {target['company']} ({target['location']})

Hi {target['recipient']},

I was reviewing {target['company']}'s work in the Kenyan renewable space and {target['hook']}.

While looking at your digital presence on mobile, I noticed an important commercial gap: over 80% of Kenyan property owners, factory directors, and commercial decision-makers now research solar contractors on their phones via Safaricom 4G/5G. Sluggish load speeds, dated layouts, and technical spec sheets often cause high-value prospects to bounce before your engineers ever receive their contact details.

At Elite Designs & Xclusive Tech, we engineer complete, custom Next-Gen Solar Web Platforms built specifically for Kenyan EPCs and renewable energy leaders—delivering sub-1.2s mobile speeds, full EPRA compliance authority, and built-in interactive financial engines.

For {target['company']} specifically, we have designed {target['pitch_focus']}, featuring:

1. Core Engineering & Speed: Built from the ground up on ultra-lightweight custom architecture (scoring 95+ on Google Mobile PageSpeed) with zero bloated WordPress plugins.
2. Flagship AI Engine: Integrated {target['ai_feature']}.
3. Automated WhatsApp Lead Routing: Every calculated sizing report or KPLC bill upload is formatted and dispatched directly to your sales engineers' WhatsApp within 3 seconds.
4. Tender Authority & Credibility: Full EPRA Contractor Class showcase, Tier-1 hardware warranty centers, and interactive filterable project portfolios (kWp installed, drone footage, and client verification).
5. Executive Brand Collateral: Branded company profile PDFs, tender presentation templates, and field installation collateral designed to win multi-million shilling corporate bids.

I have already put together an interactive mobile preview demonstrating how this architecture functions for {target['company']}.

Would you be open to a 7-minute call or quick WhatsApp walkthrough this week to review the preview? 

If so, let me know what day works best, or feel free to message me directly on WhatsApp at +254 722 753 819.

Best regards,

Dr. Samuel Kidemi
Managing Director | Elite Designs Kenya & Xclusive Tech
Phone / WhatsApp: +254 722 753 819
Email: sam@elitedesigns.co.ke
Office: Suite F8, Wood Ave Park Apartments, Kilimani, Nairobi
Web: https://elitedesigns.co.ke | https://www.xclusivetech.co.ke
"""
    return body

print("Generating 20 customized solar outreach email drafts...")
for target in TARGETS:
    filepath = os.path.join(OUTPUT_DIR, target['filename'])
    content = build_email_text(target)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Created: {filepath}")

print(f"\nAll 20 drafts successfully generated and saved to {OUTPUT_DIR}/")
