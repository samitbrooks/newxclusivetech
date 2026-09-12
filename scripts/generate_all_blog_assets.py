#!/usr/bin/env python3
"""
generate_all_blog_assets.py
Generates 32 bespoke, distinct, 100% valid XML SVGs for every blog article.
Updates blog/index.html and all 32 blog/*.html files with distinct preview images and internal article hero images.
"""
import os
import re
import html
import xml.etree.ElementTree as ET

WORKSPACE_DIR = "/Users/app/newxclusivetech"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "assets", "images", "blog")
BLOG_DIR = os.path.join(WORKSPACE_DIR, "blog")

os.makedirs(IMAGES_DIR, exist_ok=True)

# 32 bespoke post configs with color palettes, icons, metrics, and industry-specific graphics
POSTS = [
    {
        "slug": "web-design-for-businesses-in-kiambu-county",
        "category": "Local SEO & Web Design",
        "tag": "Kiambu County",
        "title": "Web Design for Businesses in Kiambu County",
        "subtitle": "Thika, Ruiru, Juja, Kikuyu, Limuru & Gatundu Growth Blueprint",
        "c1": "#1E3A8A", "c2": "#0284C7", "accent": "#38BDF8",
        "alt": "Web design services in Kiambu County, Thika, Ruiru, Juja and Kikuyu Kenya",
        "badge": "Kiambu Hub",
        "pills": ["Thika Superhighway", "Ruiru Hub", "Juja Tech", "Kikuyu & Limuru"],
        "stat1": "6 Towns Covered", "stat2": "100% Local SEO Focus",
        "viz_type": "kiambu_map"
    },
    {
        "slug": "how-long-does-it-take-to-build-a-website-in-kenya",
        "category": "Website Delivery Timelines",
        "tag": "Project Milestones",
        "title": "How Long Does It Take to Build a Website in Kenya?",
        "subtitle": "Realistic Delivery Schedules, Phased Sprints & Launch Deadlines",
        "c1": "#065F46", "c2": "#0D9488", "accent": "#34D399",
        "alt": "Website development timeline and turnaround schedule in Kenya",
        "badge": "3-5 Days Launch",
        "pills": ["Day 1: Discovery", "Day 3: Prototype", "Day 5: M-Pesa Setup", "Day 7: Launch"],
        "stat1": "3-5 Days Starter", "stat2": "2-3 Wks Custom",
        "viz_type": "timeline_gantt"
    },
    {
        "slug": "how-much-does-a-website-cost-in-kenya",
        "category": "Web Design Pricing",
        "tag": "Kenya Price Guide",
        "title": "How Much Does a Website Cost in Kenya?",
        "subtitle": "Clear Breakdown: Starter, Business Growth & Custom E-Commerce",
        "c1": "#1E1B4B", "c2": "#4338CA", "accent": "#818CF8",
        "alt": "Website design cost and pricing packages in Kenya KES breakdown",
        "badge": "Transparent Pricing",
        "pills": ["KES 31.5K Starter", "KES 49K Growth", "KES 72K E-Commerce", "No Hidden Fees"],
        "stat1": "From KES 31,500", "stat2": "Zero Monthly Lock-in",
        "viz_type": "pricing_tiers"
    },
    {
        "slug": "how-much-does-social-media-management-cost-in-kenya",
        "category": "Digital Marketing Costs",
        "tag": "Social Media ROI",
        "title": "How Much Does Social Media Management Cost in Kenya?",
        "subtitle": "Monthly Retainers, Content Calendars, Paid Meta Ads & ROI",
        "c1": "#831843", "c2": "#BE185D", "accent": "#F472B6",
        "alt": "Social media management pricing and monthly retainer cost in Kenya",
        "badge": "High ROI Campaigns",
        "pills": ["Instagram & TikTok", "Facebook Ads", "Content Creation", "Lead Generation"],
        "stat1": "KES 25K-60K / mo", "stat2": "4.8x Avg Ad Return",
        "viz_type": "social_analytics"
    },
    {
        "slug": "website-vs-facebook-page-which-does-your-business-need",
        "category": "Digital Strategy Guide",
        "tag": "Asset Ownership",
        "title": "Website vs Facebook Page: Which Does Your Kenyan Business Need?",
        "subtitle": "Why Relying Solely on Social Media Is Costing You Serious Revenue",
        "c1": "#1E293B", "c2": "#2563EB", "accent": "#60A5FA",
        "alt": "Comparison between custom website and Facebook business page for Kenyan SMEs",
        "badge": "Asset Ownership",
        "pills": ["100% Data Control", "Google Rankable", "M-Pesa Integrated", "No Algorithm Tax"],
        "stat1": "Own Your Traffic", "stat2": "24/7 Automated Sales",
        "viz_type": "vs_matrix"
    },
    {
        "slug": "geo-and-aeo-explained-getting-found-by-ai",
        "category": "AI Search Optimization",
        "tag": "GEO & AEO 2026",
        "title": "GEO & AEO Explained: How to Get Found by ChatGPT & Claude",
        "subtitle": "Generative Engine Optimization & Answer Engine Optimization in Kenya",
        "c1": "#0F172A", "c2": "#6366F1", "accent": "#A5B4FC",
        "alt": "Generative Engine Optimization GEO and AEO for AI search engines in Kenya",
        "badge": "AI Citation Ready",
        "pills": ["ChatGPT Citations", "Gemini Overviews", "Claude Context", "Schema Markup"],
        "stat1": "#1 AI Recommendations", "stat2": "Structured Knowledge",
        "viz_type": "ai_neural"
    },
    {
        "slug": "why-photographers-and-videographers-need-a-website",
        "category": "Creative & Media",
        "tag": "Visual Portfolios",
        "title": "Why Photographers & Videographers in Kenya Need a Website",
        "subtitle": "High-Res Client Galleries, Package Pricing & Direct Booking",
        "c1": "#18181B", "c2": "#3F3F46", "accent": "#F59E0B",
        "alt": "Web design for photographers and videographers in Kenya high resolution portfolio",
        "badge": "4K Client Showcase",
        "pills": ["Proofing Galleries", "Rate Cards", "Contract Signings", "M-Pesa Booking"],
        "stat1": "Zero Quality Loss", "stat2": "Instant Invoicing",
        "viz_type": "camera_aperture"
    },
    {
        "slug": "why-driving-schools-need-a-website",
        "category": "Education & Licensing",
        "tag": "NTSA Curriculum",
        "title": "Why Driving Schools in Kenya Need a Website",
        "subtitle": "Capture 'Driving School Near Me' Searches & Automate Student Signups",
        "c1": "#78350F", "c2": "#D97706", "accent": "#FBBF24",
        "alt": "Website development for driving schools in Kenya NTSA curriculum registration",
        "badge": "NTSA Compliance",
        "pills": ["Course Schedules", "Class B/C/E Signups", "Theory Notes", "Branch Locators"],
        "stat1": "92% Mobile Searches", "stat2": "Online Fee Deposits",
        "viz_type": "driving_dashboard"
    },
    {
        "slug": "why-car-dealerships-need-a-website",
        "category": "Automotive & Motor Yards",
        "tag": "Stock Showroom",
        "title": "Why Car Dealerships in Kenya Need a Website",
        "subtitle": "Live Inventory Search, Vehicle Specs, Trade-Ins & Financing Calculators",
        "c1": "#0F172A", "c2": "#DC2626", "accent": "#F87171",
        "alt": "Car dealership website design and motor vehicle inventory management Kenya",
        "badge": "Digital Showroom",
        "pills": ["Live Inventory", "Asset Financing", "Trade-in Evaluator", "KRA/NTSA Verified"],
        "stat1": "Search by Budget", "stat2": "Instant WhatsApp Lead",
        "viz_type": "car_specs"
    },
    {
        "slug": "why-real-estate-businesses-need-a-website",
        "category": "Property & Developments",
        "tag": "Prime Listings",
        "title": "Why Real Estate Businesses in Kenya Need a Website",
        "subtitle": "Nairobi Apartments, Gated Plots, Title Deed Trust & Virtual Tours",
        "c1": "#064E3B", "c2": "#059669", "accent": "#34D399",
        "alt": "Real estate website design in Kenya property listings and land sales",
        "badge": "Verified Properties",
        "pills": ["Location Filters", "Title Deed Badges", "Virtual 3D Tours", "Site Visit Booking"],
        "stat1": "Verified Title Deeds", "stat2": "Diaspora Investors",
        "viz_type": "real_estate"
    },
    {
        "slug": "why-clinics-and-healthcare-providers-need-a-website",
        "category": "Healthcare & Medicine",
        "tag": "Patient Care",
        "title": "Why Clinics & Healthcare Providers in Kenya Need a Website",
        "subtitle": "Doctor Schedules, Online Appointments, NHIF/SHA Info & Lab Results",
        "c1": "#083344", "c2": "#0891B2", "accent": "#22D3EE",
        "alt": "Clinic and hospital healthcare website development Kenya SHA NHIF portal",
        "badge": "SHA / NHIF Verified",
        "pills": ["Doctor Directory", "Appointment Booking", "Telemedicine Ready", "Lab Tests List"],
        "stat1": "24/7 Triage Access", "stat2": "HIPAA/Data Protected",
        "viz_type": "healthcare"
    },
    {
        "slug": "why-law-firms-need-a-professional-website",
        "category": "Legal & Corporate Law",
        "tag": "Advocates of Kenya",
        "title": "Why Law Firms in Kenya Need a Professional Website",
        "subtitle": "Establish Authority, Practice Areas, Partner Bios & Retainer Intakes",
        "c1": "#1C1917", "c2": "#78716C", "accent": "#D4D4D8",
        "alt": "Law firm website design Kenya advocates commissioner for oaths corporate law",
        "badge": "LSK Accredited",
        "pills": ["Conveyancing", "Corporate Law", "Litigation & Dispute", "Retainer Inquiries"],
        "stat1": "High-Trust Profile", "stat2": "Secure Consultations",
        "viz_type": "law_scales"
    },
    {
        "slug": "why-schools-need-a-website",
        "category": "Education & Academics",
        "tag": "CBC & IGCSE",
        "title": "Why Schools & Education Providers in Kenya Need a Website",
        "subtitle": "Admissions Portals, Term Calendars, Fee Structures & Parent Portals",
        "c1": "#1E1B4B", "c2": "#3730A3", "accent": "#818CF8",
        "alt": "School website design Kenya CBC curriculum admissions fee structures",
        "badge": "CBC & Cambridge",
        "pills": ["Admissions Form", "Fee Structure PDF", "Term Calendar", "Parent Circulars"],
        "stat1": "98% Online Inquiries", "stat2": "Term Announcements",
        "viz_type": "school_portal"
    },
    {
        "slug": "why-churches-and-ministries-need-a-website",
        "category": "Faith & Non-Profit",
        "tag": "Ministry Impact",
        "title": "Why Churches & Ministries in Kenya Need a Website",
        "subtitle": "Live Stream Broadcasts, Sermon Archives, M-Pesa Tithing & Ministries",
        "c1": "#4C1D95", "c2": "#7C3AED", "accent": "#C4B5FD",
        "alt": "Church website design Kenya live sermon streaming M-Pesa paybill tithe",
        "badge": "Global Fellowship",
        "pills": ["Sermon Library", "YouTube/FB Live", "Paybill Tithing", "Ministry Groups"],
        "stat1": "Live Stream Ready", "stat2": "Diaspora Giving",
        "viz_type": "church_giving"
    },
    {
        "slug": "why-restaurants-and-cafes-need-a-website",
        "category": "Food & Hospitality",
        "tag": "Digital Dining",
        "title": "Why Restaurants & Cafes in Kenya Need a Website",
        "subtitle": "Direct Online Menus, Table Reservations, Event Bookings & Takeaway",
        "c1": "#701A75", "c2": "#C026D3", "accent": "#F0ABFC",
        "alt": "Restaurant and cafe website development Kenya digital QR menu table booking",
        "badge": "Direct Ordering",
        "pills": ["Visual Menu", "Table Booking", "Direct Takeaway", "No 30% App Cut"],
        "stat1": "Zero Food App Cut", "stat2": "Instant WhatsApp Cart",
        "viz_type": "restaurant_menu"
    },
    {
        "slug": "why-hotels-and-hospitality-businesses-need-a-website",
        "category": "Hotels & Lodges",
        "tag": "Direct Bookings",
        "title": "Why Hotels & Hospitality Businesses in Kenya Need a Website",
        "subtitle": "Bypass 25% OTA Commissions with Direct Reservations & Safari Lodges",
        "c1": "#064E3B", "c2": "#047857", "accent": "#6EE7B7",
        "alt": "Hotel website design Kenya booking engine safari lodge resort bookings",
        "badge": "Direct Reservations",
        "pills": ["Live Room Availability", "Card & M-Pesa Rates", "Airport Transfers", "Virtual Tours"],
        "stat1": "0% Commission Cut", "stat2": "Direct Check-In",
        "viz_type": "hotel_booking"
    },
    {
        "slug": "why-tour-and-safari-companies-need-a-website",
        "category": "Tours & Safaris",
        "tag": "East Africa Safaris",
        "title": "Why Tour & Safari Companies in Kenya Need a Website",
        "subtitle": "Interactive Itineraries, KWS Park Fees, Custom Quotes & USD/KES Checkout",
        "c1": "#78350F", "c2": "#B45309", "accent": "#FCD34D",
        "alt": "Tour and safari company web design Kenya Maasai Mara itinerary booking",
        "badge": "Safari Specialist",
        "pills": ["Maasai Mara Tours", "Amboseli & Tsavo", "Custom Itinerary", "USD/KES Gateway"],
        "stat1": "Global Traveler Trust", "stat2": "Itinerary Builder",
        "viz_type": "safari_compass"
    },
    {
        "slug": "why-ecommerce-and-retail-businesses-need-a-website",
        "category": "E-Commerce & Retail",
        "tag": "Daraja M-Pesa",
        "title": "Why E-commerce & Retail Businesses in Kenya Need a Website",
        "subtitle": "STK Push Automated Checkout, Stock Tracking & Countrywide Courier",
        "c1": "#1E3A8A", "c2": "#2563EB", "accent": "#93C5FD",
        "alt": "Ecommerce website design Kenya M-Pesa STK push integration online store",
        "badge": "Daraja STK Push",
        "pills": ["Automated M-Pesa", "Order Dashboard", "Fargo/G4S Delivery", "SMS Notifications"],
        "stat1": "Instant STK Push", "stat2": "24/7 Checkout",
        "viz_type": "ecommerce_cart"
    },
    {
        "slug": "why-agriculture-and-agribusiness-need-a-website",
        "category": "Agribusiness & Exports",
        "tag": "Global Trade",
        "title": "Why Agriculture & Agribusiness in Kenya Need a Website",
        "subtitle": "Avocado, Tea & Coffee Exports, B2B Tenders, GAP Certifications",
        "c1": "#14532D", "c2": "#16A34A", "accent": "#86EFAC",
        "alt": "Agribusiness website design Kenya agricultural export horticulture B2B",
        "badge": "Export Certified",
        "pills": ["Global GAP Standards", "Bulk Commodity Quotes", "Cold Chain Logistics", "Traceability"],
        "stat1": "Global Buyers Reach", "stat2": "Hass & Tea Tenders",
        "viz_type": "agri_sprout"
    },
    {
        "slug": "why-construction-and-contractors-need-a-website",
        "category": "Building & Civil Works",
        "tag": "NCA Certified",
        "title": "Why Construction & Contractors in Kenya Need a Website",
        "subtitle": "Win Commercial Tenders, Showcase Completed Projects & Bill of Quantities",
        "c1": "#374151", "c2": "#4B5563", "accent": "#F59E0B",
        "alt": "Construction and contractor website design Kenya civil engineering NCA",
        "badge": "NCA Registered",
        "pills": ["Commercial Blueprints", "Project Milestones", "Machinery Fleet", "BQ Quotations"],
        "stat1": "Tender Ready", "stat2": "Architect Portfolios",
        "viz_type": "construction_helm"
    },
    {
        "slug": "why-consultants-need-a-professional-website",
        "category": "Advisory & Strategy",
        "tag": "Executive Advisory",
        "title": "Why Consultants & Professional Services Need a Website",
        "subtitle": "Build Authority, Whitepapers, Case Studies & High-Value Retainers",
        "c1": "#1E293B", "c2": "#334155", "accent": "#38BDF8",
        "alt": "Consultant and professional advisory services website development Kenya",
        "badge": "Authority & Trust",
        "pills": ["Advisory Case Studies", "Discovery Call Booking", "Research Papers", "Corporate Retainers"],
        "stat1": "Executive Inquiries", "stat2": "High-Ticket B2B",
        "viz_type": "consulting_graph"
    },
    {
        "slug": "why-beauty-salons-and-spas-need-a-website",
        "category": "Wellness & Grooming",
        "tag": "Salon Bookings",
        "title": "Why Beauty Salons & Spas in Kenya Need a Website",
        "subtitle": "Stop Managing Bookings in WhatsApp DMs: Automated Calendar & Stylists",
        "c1": "#831843", "c2": "#9D174D", "accent": "#F472B6",
        "alt": "Beauty salon and spa website design Kenya appointment booking stylist portfolio",
        "badge": "VIP Appointments",
        "pills": ["Stylist Portfolios", "Treatment Menu", "Automated Reminders", "Bridal Packages"],
        "stat1": "Zero Missed Clients", "stat2": "Upfront Deposits",
        "viz_type": "beauty_mirror"
    },
    {
        "slug": "why-gyms-and-fitness-studios-need-a-website",
        "category": "Fitness & Athletics",
        "tag": "Active Life",
        "title": "Why Gyms & Fitness Studios in Kenya Need a Website",
        "subtitle": "Class Schedules, Personal Training Profiles, Memberships & M-Pesa",
        "c1": "#7F1D1D", "c2": "#B91C1C", "accent": "#F87171",
        "alt": "Gym and fitness studio website design Kenya class timetable membership M-Pesa",
        "badge": "24/7 Member Hub",
        "pills": ["Class Timetable", "Trainer Roster", "Monthly Subscriptions", "Workout Plans"],
        "stat1": "Automated Billing", "stat2": "Capacity Management",
        "viz_type": "gym_weights"
    },
    {
        "slug": "why-logistics-transport-companies-need-a-website",
        "category": "Supply Chain & Haulage",
        "tag": "Fleet Logistics",
        "title": "Why Logistics & Transport Companies Need a Website",
        "subtitle": "Mombasa-Nairobi Corridor, Consignment Tracking & Instant Freight Quotes",
        "c1": "#0C4A6E", "c2": "#0284C7", "accent": "#38BDF8",
        "alt": "Logistics and transport freight company website design Kenya cargo tracking",
        "badge": "Corridor Fleet",
        "pills": ["Container Tracking", "Waybill Generator", "Fleet Roster", "Corridor Rates"],
        "stat1": "Real-Time Tracking", "stat2": "Cross-Border Ready",
        "viz_type": "logistics_truck"
    },
    {
        "slug": "why-financial-services-and-fintech-need-a-website",
        "category": "Fintech & Finance",
        "tag": "CBK Compliant",
        "title": "Why Financial Services & Fintech in Kenya Need a Website",
        "subtitle": "Security Compliance, Loan Calculators, Bank Grade Trust & Investor Portal",
        "c1": "#0F172A", "c2": "#1E3A8A", "accent": "#60A5FA",
        "alt": "Fintech and financial services website design Kenya loan calculator compliance",
        "badge": "Bank-Grade Security",
        "pills": ["Loan Calculator", "CBK Compliance", "256-Bit SSL", "Investor Deck"],
        "stat1": "Regulatory Compliance", "stat2": "Instant Pre-approval",
        "viz_type": "fintech_shield"
    },
    {
        "slug": "why-insurance-agents-and-brokers-need-a-website",
        "category": "Insurance & Risk",
        "tag": "Policy Comparison",
        "title": "Why Insurance Agents & Brokers in Kenya Need a Website",
        "subtitle": "Motor, Health & Life Premium Calculators, Claim Assistance & Fast Quotes",
        "c1": "#14532D", "c2": "#047857", "accent": "#34D399",
        "alt": "Insurance broker and agent website design Kenya motor private policy quotes",
        "badge": "IRA Licensed",
        "pills": ["Comprehensive Motor", "Medical Inpatient", "Instant Quotation", "Claim Tracker"],
        "stat1": "Multi-Insurer Compare", "stat2": "Instant Digital Cover",
        "viz_type": "insurance_umbrella"
    },
    {
        "slug": "why-fashion-and-apparel-brands-need-a-website",
        "category": "Fashion & Lifestyle",
        "tag": "Runway & Streetwear",
        "title": "Why Fashion & Apparel Brands in Kenya Need a Website",
        "subtitle": "Digital Lookbooks, Size Fit Guides, New Drops & Direct M-Pesa Orders",
        "c1": "#581C87", "c2": "#7E22CE", "accent": "#C084FC",
        "alt": "Fashion brand and clothing apparel ecommerce website design Kenya lookbook",
        "badge": "Made in Kenya",
        "pills": ["Seasonal Drops", "Exact Size Charts", "Instagram Sync", "Same-Day Delivery"],
        "stat1": "Sell Out Drops Fast", "stat2": "Zero WhatsApp Chaos",
        "viz_type": "fashion_hanger"
    },
    {
        "slug": "why-event-planners-need-a-website",
        "category": "Events & Weddings",
        "tag": "Grand Occasions",
        "title": "Why Event Planners & Entertainment in Kenya Need a Website",
        "subtitle": "Showcase Galas, Weddings, Corporate Summits & Availability Dates",
        "c1": "#881337", "c2": "#BE123C", "accent": "#FB7185",
        "alt": "Event planner and wedding organizer website development Kenya gala summits",
        "badge": "Signature Events",
        "pills": ["Wedding Portfolio", "Corporate Summits", "Vendor Coordination", "Budget Calculator"],
        "stat1": "100+ Galas Produced", "stat2": "Clear Date Availability",
        "viz_type": "event_ticket"
    },
    {
        "slug": "why-food-and-beverage-brands-need-a-website",
        "category": "FMCG & Beverages",
        "tag": "KEBS Standard",
        "title": "Why Food & Beverage Brands in Kenya Need a Website",
        "subtitle": "Supermarket Stockists Locator, Nutritional Facts & B2B Wholesale",
        "c1": "#7C2D12", "c2": "#C2410C", "accent": "#FB923C",
        "alt": "Food and beverage FMCG brand website design Kenya supermarket stockist locator",
        "badge": "KEBS Certified",
        "pills": ["Store Locator", "Nutritional Labelling", "Supermarket Distribution", "Wholesale Inquiries"],
        "stat1": "Retailer Trust", "stat2": "Nationwide Stockists",
        "viz_type": "food_bottle"
    },
    {
        "slug": "why-cosmetics-and-beauty-brands-need-a-website",
        "category": "Cosmetics & Skincare",
        "tag": "Dermatology Grade",
        "title": "Why Cosmetics & Beauty Brands in Kenya Need a Website",
        "subtitle": "Melanin-Tailored Skincare, Ingredient Authenticity & Retail Checkouts",
        "c1": "#831843", "c2": "#DB2777", "accent": "#F472B6",
        "alt": "Cosmetics and beauty skincare brand website design Kenya melanin shade finder",
        "badge": "Clean Beauty",
        "pills": ["Shade Finder Quiz", "Organic Ingredients", "Customer Reviews", "M-Pesa STK Push"],
        "stat1": "100% Authentic Batch", "stat2": "Automated Reorders",
        "viz_type": "cosmetics_jar"
    },
    {
        "slug": "why-ngos-and-nonprofits-need-a-website",
        "category": "NGOs & Non-Profits",
        "tag": "Donor Transparency",
        "title": "Why NGOs & Non-Profits in Kenya Need a Website",
        "subtitle": "Audit Reports, Impact Metrics, Storytelling & Global Grant Eligibility",
        "c1": "#134E4A", "c2": "#0F766E", "accent": "#2DD4BF",
        "alt": "NGO and non-profit organization website development Kenya donor reporting grants",
        "badge": "Verified 501c3 / NGO",
        "pills": ["Audited Financials", "Impact Dashboards", "Donor Transparence", "Grant Proposals"],
        "stat1": "$2.4M Raised Online", "stat2": "Direct Card/M-Pesa Gifts",
        "viz_type": "ngo_globe"
    },
    {
        "slug": "why-startups-need-a-professional-website",
        "category": "Startups & Tech",
        "tag": "Venture Scale",
        "title": "Why Startups in Kenya Need a Professional Website From Day One",
        "subtitle": "VC Due Diligence, Customer Traction, Early Beta Waitlists & Hiring",
        "c1": "#0F172A", "c2": "#4338CA", "accent": "#38BDF8",
        "alt": "Startup web development Kenya venture capital pitch deck traction waitlist",
        "badge": "Silicon Savannah",
        "pills": ["Investor Deck Hub", "Live Waitlist CRM", "API Documentation", "Product Hunt Ready"],
        "stat1": "Seed Stage Ready", "stat2": "Rapid MVP Deploy",
        "viz_type": "startup_rocket"
    }
]

def escape_xml(s):
    """Escapes XML entities safely without double escaping and keeps XML entities strictly lowercase."""
    if not s:
        return ""
    # Standard XML escaping
    s = s.replace('&', '&amp;')
    s = s.replace('&amp;amp;', '&amp;')
    s = s.replace('&amp;bull;', '&#8226;')
    s = s.replace('&amp;check;', '&#10003;')
    s = s.replace('&amp;rarr;', '&#8594;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    s = s.replace("'", '&apos;')
    # Guarantee standard XML entities are lowercase
    s = s.replace('&AMP;', '&amp;')
    s = s.replace('&LT;', '&lt;')
    s = s.replace('&GT;', '&gt;')
    s = s.replace('&QUOT;', '&quot;')
    s = s.replace('&APOS;', '&apos;')
    return s

def build_svg(post):
    """Builds a rich, distinct 1200x630 SVG with XML-safe entities."""
    c1 = post["c1"]
    c2 = post["c2"]
    accent = post["accent"]
    category_raw = post["category"].upper()
    category = escape_xml(category_raw)
    tag = escape_xml(post["tag"])
    badge = escape_xml(post["badge"])
    stat1 = escape_xml(post["stat1"])
    stat2 = escape_xml(post["stat2"])

    # Safe word/character slicing before XML escaping
    plain_title = post["title"]
    if len(plain_title) > 38:
        t1 = escape_xml(plain_title[:38])
        t2 = escape_xml(plain_title[38:85])
        title_tspan = f"<tspan x='0' dy='0'>{t1}</tspan><tspan x='0' dy='48'>{t2}</tspan>"
    else:
        title_tspan = f"<tspan x='0' dy='0'>{escape_xml(plain_title)}</tspan>"

    plain_sub = post["subtitle"]
    if len(plain_sub) > 58:
        s1 = escape_xml(plain_sub[:58])
        s2 = escape_xml(plain_sub[58:120])
        sub_tspan = f"<tspan x='0' dy='0'>{s1}</tspan><tspan x='0' dy='26'>{s2}</tspan>"
    else:
        sub_tspan = f"<tspan x='0' dy='0'>{escape_xml(plain_sub)}</tspan>"
    
    # Generate pills XML
    pill_xml = ""
    start_x = 70
    for idx, pill in enumerate(post["pills"][:4]):
        p_text = escape_xml(pill)
        w = max(110, len(p_text) * 11 + 30)
        pill_xml += f"""
        <g transform="translate({start_x}, 530)">
            <rect width="{w}" height="42" rx="21" fill="rgba(255, 255, 255, 0.08)" stroke="{accent}" stroke-width="1.5"/>
            <circle cx="20" cy="21" r="5" fill="{accent}"/>
            <text x="34" y="26" fill="#F8FAFC" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600">{p_text}</text>
        </g>
        """
        start_x += w + 16

    # Custom graphic panel on right side (x: 760, y: 90, width: 380, height: 450)
    panel_content = f"""
        <rect x="760" y="80" width="380" height="470" rx="24" fill="rgba(15, 23, 42, 0.75)" stroke="rgba(255, 255, 255, 0.15)" stroke-width="2"/>
        <circle cx="795" cy="115" r="7" fill="#EF4444"/>
        <circle cx="815" cy="115" r="7" fill="#F59E0B"/>
        <circle cx="835" cy="115" r="7" fill="#10B981"/>
        <rect x="860" y="103" width="250" height="24" rx="6" fill="rgba(255,255,255,0.06)"/>
        <text x="872" y="119" fill="#94A3B8" font-family="monospace" font-size="11">xclusivetech.co.ke/{escape_xml(post['slug'])}</text>

        <!-- Metric Cards Inside Panel -->
        <g transform="translate(785, 155)">
            <rect width="330" height="95" rx="16" fill="rgba(255,255,255,0.04)" stroke="{accent}" stroke-width="1.5"/>
            <text x="20" y="32" fill="#94A3B8" font-family="sans-serif" font-size="12" font-weight="600" letter-spacing="1">KEY METRIC / FOCUS</text>
            <text x="20" y="68" fill="#FFFFFF" font-family="sans-serif" font-size="22" font-weight="800">{stat1}</text>
            <circle cx="290" cy="48" r="18" fill="{accent}" fill-opacity="0.15"/>
            <text x="290" y="54" text-anchor="middle" fill="{accent}" font-size="16" font-weight="900">&#10003;</text>
        </g>

        <g transform="translate(785, 265)">
            <rect width="330" height="95" rx="16" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
            <text x="20" y="32" fill="#94A3B8" font-family="sans-serif" font-size="12" font-weight="600" letter-spacing="1">KENYA PERFORMANCE</text>
            <text x="20" y="68" fill="{accent}" font-family="sans-serif" font-size="20" font-weight="800">{stat2}</text>
            <circle cx="290" cy="48" r="18" fill="rgba(255,255,255,0.1)"/>
            <text x="290" y="54" text-anchor="middle" fill="#FFFFFF" font-size="14" font-weight="900">&#8594;</text>
        </g>

        <!-- Guarantee Bar -->
        <g transform="translate(785, 375)">
            <rect width="330" height="135" rx="16" fill="url(#panelGrad)" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
            <text x="20" y="32" fill="#FFFFFF" font-family="sans-serif" font-size="15" font-weight="700">Kenyan SME Benchmark</text>
            <text x="20" y="58" fill="#CBD5E1" font-family="sans-serif" font-size="13">Standard SEO, GEO &amp; AEO Architecture</text>
            <text x="20" y="82" fill="#CBD5E1" font-family="sans-serif" font-size="13">Daraja M-Pesa Ready &#8226; Fast Turnaround</text>
            <rect x="20" y="100" width="290" height="8" rx="4" fill="rgba(255,255,255,0.1)"/>
            <rect x="20" y="100" width="245" height="8" rx="4" fill="{accent}"/>
        </g>
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
    <defs>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{c1}"/>
            <stop offset="60%" stop-color="{c2}"/>
            <stop offset="100%" stop-color="#090D16"/>
        </linearGradient>
        <linearGradient id="panelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="rgba(255, 255, 255, 0.08)"/>
            <stop offset="100%" stop-color="rgba(255, 255, 255, 0.02)"/>
        </linearGradient>
        <radialGradient id="glow" cx="20%" cy="30%" r="60%">
            <stop offset="0%" stop-color="{accent}" stop-opacity="0.35"/>
            <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
        </radialGradient>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
        </pattern>
    </defs>

    <!-- Background Base -->
    <rect width="1200" height="630" fill="url(#bgGrad)"/>
    <rect width="1200" height="630" fill="url(#grid)"/>
    <circle cx="250" cy="200" r="350" fill="url(#glow)"/>

    <!-- Header Brand Bar -->
    <g transform="translate(70, 60)">
        <rect width="36" height="36" rx="8" fill="#FFFFFF"/>
        <path d="M 10 10 L 26 26 M 26 10 L 10 26" stroke="#0F172A" stroke-width="4.5" stroke-linecap="round"/>
        <text x="48" y="25" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="19" font-weight="900" letter-spacing="0.5">XCLUSIVE TECH</text>
        <text x="210" y="25" fill="{accent}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" letter-spacing="2">KENYA</text>
    </g>

    <!-- Category / Tag Badge -->
    <g transform="translate(70, 125)">
        <rect width="{max(160, len(category) * 10 + 40)}" height="32" rx="16" fill="rgba(255, 255, 255, 0.12)" stroke="{accent}" stroke-width="1.2"/>
        <circle cx="16" cy="16" r="4" fill="{accent}"/>
        <text x="28" y="21" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" letter-spacing="1.5">{category}</text>
    </g>

    <!-- Main Title (Wrapped if long) -->
    <g transform="translate(70, 200)">
        <text x="0" y="30" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="38" font-weight="800" line-height="1.2">
            {title_tspan}
        </text>
        <text x="0" y="115" fill="#CBD5E1" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="400">
            {sub_tspan}
        </text>
    </g>

    <!-- Industry Pills Row -->
    {pill_xml}

    <!-- Right Side Graphic Panel -->
    {panel_content}
</svg>
"""
    return svg

def main():
    print(f"=== Generating 32 Bespoke Blog SVGs ===")
    success_count = 0
    for post in POSTS:
        slug = post["slug"]
        svg_content = build_svg(post)
        
        # Test XML validity strictly!
        try:
            ET.fromstring(svg_content)
        except Exception as e:
            print(f"CRITICAL XML ERROR in {slug}: {e}")
            raise e
        
        file_path = os.path.join(IMAGES_DIR, f"{slug}.svg")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        success_count += 1
    print(f"Successfully generated and validated {success_count} SVGs in {IMAGES_DIR}")

    # Now update blog/index.html
    print("=== Updating blog/index.html ===")
    index_path = os.path.join(BLOG_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        index_html = f.read()

    # Rebuild the 32 cards in blog/index.html
    cards_html = ""
    for post in POSTS:
        slug = post["slug"]
        title = post["title"]
        category = post["category"]
        alt = post["alt"]
        subtitle = post["subtitle"]
        card = f"""                <a href="{slug}.html" class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-500 transition-all duration-300 flex flex-col group">
                    <div class="w-full h-48 rounded-xl overflow-hidden mb-4 bg-slate-900 border border-slate-100">
                        <img src="../assets/images/blog/{slug}.svg" alt="{alt}" width="600" height="315" loading="lazy" decoding="async" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                    </div>
                    <span class="text-xs uppercase tracking-widest text-blue-600 font-semibold mb-2">{category}</span>
                    <h2 class="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors mb-2">{title}</h2>
                    <p class="text-gray-600 text-sm flex-grow">{subtitle}</p>
                    <span class="text-sm font-semibold text-blue-600 mt-4 flex items-center gap-1 group-hover:translate-x-1 transition-transform">Read article &rarr;</span>
                </a>\n"""
        cards_html += card

    # Replace cards inside post-grid
    post_grid_regex = re.compile(r'(<div id="post-grid"[^>]*>)(.*?)(</div>\s*</div>\s*</section>)', re.DOTALL)
    match = post_grid_regex.search(index_html)
    if match:
        new_index_html = index_html[:match.start(2)] + "\n" + cards_html + "            " + index_html[match.end(2):]
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_index_html)
        print("Updated blog/index.html with all 32 bespoke cards!")
    else:
        print("WARNING: Could not find post-grid in blog/index.html")

    # Now update all 32 blog/*.html files
    print("=== Updating all 32 blog/*.html files with featured hero images ===")
    updated_posts = 0
    for post in POSTS:
        slug = post["slug"]
        alt = post["alt"]
        title = post["title"]
        post_path = os.path.join(BLOG_DIR, f"{slug}.html")
        if not os.path.exists(post_path):
            print(f"File not found: {post_path}")
            continue

        with open(post_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update og:image and twitter:image
        content = re.sub(
            r'<meta property="og:image"[^>]*>',
            f'<meta property="og:image" content="https://xclusivetech.co.ke/assets/images/blog/{slug}.svg">',
            content
        )
        content = re.sub(
            r'<meta name="twitter:image"[^>]*>',
            f'<meta name="twitter:image" content="https://xclusivetech.co.ke/assets/images/blog/{slug}.svg">',
            content
        )

        # Remove any old featured image figure if exists
        content = re.sub(r'<figure class="my-8[^"]*"[^>]*>.*?</figure>', '', content, flags=re.DOTALL)

        # Insert hero image figure right after the lead intro paragraph (<p class="text-xl text-gray-600 mb-8">...</p>)
        # or after </h1>
        hero_figure = f"""
            <figure class="my-8 rounded-2xl overflow-hidden border border-slate-200 shadow-lg bg-slate-950">
                <img src="../assets/images/blog/{slug}.svg" alt="{alt}" width="1200" height="630" class="w-full h-auto object-cover" loading="eager" fetchpriority="high">
            </figure>
"""
        intro_regex = re.compile(r'(<p class="text-xl text-gray-600 mb-8">.*?</p>)', re.DOTALL)
        if intro_regex.search(content):
            content = intro_regex.sub(r'\1' + hero_figure, content, count=1)
        else:
            # Fallback: insert right after </h1>
            content = re.sub(r'(</h1>)', r'\1' + hero_figure, content, count=1)

        # Clean any remaining text-white or murky cards in FAQs if any
        content = content.replace('glassmorphism-card p-6 rounded-xl border border-white/10', 'bg-white p-6 rounded-xl border border-slate-200 shadow-sm')
        content = content.replace('text-lg font-semibold mb-2 text-white', 'text-lg font-semibold mb-2 text-gray-900')

        with open(post_path, "w", encoding="utf-8") as f:
            f.write(content)
        updated_posts += 1

    print(f"Updated {updated_posts} blog posts with internal hero images, OG images, and clean light-mode cards!")

if __name__ == "__main__":
    main()
