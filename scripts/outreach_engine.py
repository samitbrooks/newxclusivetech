#!/usr/bin/env python3
"""
Xclusive Tech — Automated Outbound Lead Generation & Cold Email Engine
----------------------------------------------------------------------
Generates personalized, high-converting cold emails and follow-ups for target
niches (Tourism, E-Commerce, Professional Services, Agencies) and books
discovery calls via WhatsApp / Calendar.

Usage:
  python3 scripts/outreach_engine.py --dry-run
  python3 scripts/outreach_engine.py --dry-run --save-drafts
  python3 scripts/outreach_engine.py --send --smtp-host ... --smtp-user ...
"""

import os
import sys
import csv
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Default Xclusive Tech Configuration
DEFAULT_SENDER_NAME = "Samuel Kidemi | Xclusive Tech"
DEFAULT_SENDER_EMAIL = "hello@xclusivetech.co.ke"
DEFAULT_WHATSAPP_BOOKING = "https://wa.me/254722753819?text=Hi%20Samuel,%20I%20got%20your%20email%20and%20would%20like%20to%20book%20a%20quick%20discovery%20call."
DEFAULT_CALENDAR_BOOKING = "https://wa.me/254722753819?text=Hi%20Samuel,%20let%27s%20schedule%20a%2015-min%20call"

# Email Templates tailored to specific ICP niches
TEMPLATES = {
    "tourism": {
        "subject": "Book a 10-min Call: Safari booking flow & conversion for {website}",
        "body": """Hi {contact_name},

I was looking at {company_name} online and noticed you have great safari packages and itineraries.

While browsing, I {personalized_observation}.

In our work engineering web systems for tourism brands (including Santorini Queen luxury charters and Diani Elite Taxi), we found that over 78% of travelers in Kenya browse on mobile. Trimming load speed below 1.5 seconds and adding automated M-Pesa + card deposit checkouts typically lifts direct booking inquiries by 35%+.

Would you be open to a quick 10-minute discovery call this week? I can share a free 3-point conversion audit of {website} with zero obligation.

You can book a call with me directly here:
👉 WhatsApp: {booking_link}
👉 Or simply reply to this email with a time that works best for you.

Best regards,

Samuel Kidemi
Lead Software Engineer & Co-Founder | Xclusive Tech
Co-Founder, Top Digitally Fit Web Design Firm of the Year
Kilimani, Nairobi, Kenya
Phone / WhatsApp: +254 722 753 819
Website: https://www.xclusivetech.co.ke
"""
    },
    "retail_ecommerce": {
        "subject": "Book a 10-min Call: Automating M-Pesa checkouts for {company_name}",
        "body": """Hi {contact_name},

I came across {company_name} and love your product selection and brand momentum.

However, I {personalized_observation}.

When shoppers have to manually DM or ask for payment instructions, up to 45% of potential orders drop off—especially late at night or during peak campaigns.

At Xclusive Tech, we engineer ultra-fast e-commerce platforms with automated Safaricom Daraja 2.0 M-Pesa STK push. Customers enter their phone number, tap their PIN on their phone, and the order is instantly validated with automated WhatsApp receipts—zero manual messaging required.

Would you be open to a 10-minute call to see a live 60-second checkout demo?

👉 Book a call on WhatsApp: {booking_link}
👉 Or reply here and let me know when suits you.

Best regards,

Samuel Kidemi
Lead Software Engineer & Co-Founder | Xclusive Tech
120+ High-Performance Web Systems Delivered
Kilimani, Nairobi, Kenya
WhatsApp: +254 722 753 819 | https://www.xclusivetech.co.ke
"""
    },
    "professional_services": {
        "subject": "Book a 10-min Call: Website conversion & local search ranking for {company_name}",
        "body": """Hi {contact_name},

I hope you are having a productive week.

I was reviewing established firms in your sector and visited {website}. I {personalized_observation}.

High-value clients in Nairobi search with high intent—often asking Google or AI assistants for recommendations in Westlands, Kilimani, and Upper Hill. Without modern schema markup and sub-1.5s mobile speed, potential clients easily drift to competitors.

We specialize in high-converting web engineering and modern search architecture (awarded Co-Founder of the Top Digitally Fit Web Design Firm of the Year). 

Could we do a brief 10-minute call to walk you through a complimentary digital audit of {website}?

👉 Book directly: {booking_link}
👉 Or let me know what day works for you.

Best regards,

Samuel Kidemi
Lead Software Engineer & Co-Founder | Xclusive Tech
Office: Wood Ave, Kilimani, Nairobi
Phone / WhatsApp: +254 722 753 819
https://www.xclusivetech.co.ke
"""
    },
    "agency_crm": {
        "subject": "Book a 10-min Call: Streamlining lead tracking and M-Pesa billing for {company_name}",
        "body": """Hi {contact_name},

Running an active service business in Kenya means juggling leads from WhatsApp, Instagram, and web forms—and manual follow-up always leads to lost deals.

I {personalized_observation}.

We built Frostwood CRM specifically for Kenyan agencies, consultants, and contractors to solve this:
- Consolidates incoming leads into one clear visual pipeline.
- Generates professional PDF invoices with automated Safaricom Daraja M-Pesa STK push.
- Prevents leads from slipping through the cracks.

Would you be open to a quick 10-minute walkthrough call to see how Frostwood CRM can save your team 5+ hours every week?

👉 Schedule a call via WhatsApp: {booking_link}
👉 Or reply directly to this email.

Best regards,

Samuel Kidemi
Lead Software Engineer & Co-Founder | Xclusive Tech
Creator of Frostwood CRM (https://www.xclusivetech.co.ke/frostwoodcrm)
WhatsApp: +254 722 753 819
"""
    }
}

def render_email(lead: dict, booking_link: str) -> dict:
    niche = lead.get("niche", "professional_services").strip().lower()
    tpl = TEMPLATES.get(niche, TEMPLATES["professional_services"])
    
    context = {
        "company_name": lead.get("company_name", "your business").strip(),
        "contact_name": lead.get("contact_name", "there").strip(),
        "website": lead.get("website", "your website").strip(),
        "personalized_observation": lead.get("personalized_observation", "spotted a few areas to optimize mobile conversion and inquiry speed").strip(),
        "booking_link": booking_link
    }
    
    subject = tpl["subject"].format(**context)
    body = tpl["body"].format(**context)
    return {"subject": subject, "body": body}

def send_smtp_email(smtp_cfg: dict, to_email: str, subject: str, body: str, sender_name: str, sender_email: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    
    part = MIMEText(body, "plain", "utf-8")
    msg.attach(part)
    
    port = int(smtp_cfg.get("port", 587))
    server = smtplib.SMTP(smtp_cfg["host"], port)
    server.ehlo()
    if port == 587:
        server.starttls()
    if smtp_cfg.get("user") and smtp_cfg.get("password"):
        server.login(smtp_cfg["user"], smtp_cfg["password"])
    server.sendmail(sender_email, [to_email], msg.as_string())
    server.quit()

def main():
    parser = argparse.ArgumentParser(description="Xclusive Tech Outbound Email Engine")
    parser.add_argument("--csv", default="scripts/leads_sample.csv", help="Path to leads CSV file")
    parser.add_argument("--dry-run", action="store_true", help="Preview generated emails without sending")
    parser.add_argument("--save-drafts", action="store_true", help="Save drafted emails to outreach_drafts/ directory")
    parser.add_argument("--send", action="store_true", help="Send emails via SMTP")
    parser.add_argument("--booking-link", default=DEFAULT_WHATSAPP_BOOKING, help="Booking link (WhatsApp or Cal.com/Calendly)")
    parser.add_argument("--smtp-host", default=os.getenv("SMTP_HOST", ""), help="SMTP Host")
    parser.add_argument("--smtp-port", default=os.getenv("SMTP_PORT", "587"), help="SMTP Port")
    parser.add_argument("--smtp-user", default=os.getenv("SMTP_USER", ""), help="SMTP Username / Email")
    parser.add_argument("--smtp-pass", default=os.getenv("SMTP_PASS", ""), help="SMTP Password / App Password")
    parser.add_argument("--sender-email", default=DEFAULT_SENDER_EMAIL, help="Sender email address")
    parser.add_argument("--sender-name", default=DEFAULT_SENDER_NAME, help="Sender display name")
    
    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print(f"Error: CSV file not found at {args.csv}")
        sys.exit(1)

    leads = []
    with open(args.csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)

    print(f"\n=======================================================")
    print(f"  Xclusive Tech Outbound Campaign Engine")
    print(f"  Loaded {len(leads)} leads from {args.csv}")
    print(f"  Booking Link: {args.booking_link}")
    print(f"=======================================================\n")

    if args.save_drafts:
        os.makedirs("outreach_drafts", exist_ok=True)

    sent_count = 0
    draft_count = 0

    for i, lead in enumerate(leads, 1):
        rendered = render_email(lead, args.booking_link)
        status = lead.get("status", "PENDING")
        company = lead.get("company_name", "Unknown")
        email = lead.get("email", "")

        print(f"[{i}/{len(leads)}] {company} ({email}) - Niche: {lead.get('niche')} - Status: {status}")
        print(f"      Subject: {rendered['subject']}")

        if args.save_drafts:
            safe_comp = "".join([c if c.isalnum() else "_" for c in company])
            filename = f"outreach_drafts/{i:02d}_{safe_comp}.txt"
            with open(filename, "w", encoding="utf-8") as df:
                df.write(f"To: {email}\n")
                df.write(f"Subject: {rendered['subject']}\n\n")
                df.write(rendered["body"])
            print(f"      Draft saved: {filename}")

        if args.dry_run or not args.send:
            print(f"      [DRY-RUN / PREVIEW MODE - Not sent]")
            draft_count += 1
        elif args.send:
            if not args.smtp_host or not args.smtp_user:
                print("      Error: --send requires --smtp-host and --smtp-user (or SMTP_HOST, SMTP_USER env vars).")
                continue
            try:
                smtp_cfg = {
                    "host": args.smtp_host,
                    "port": args.smtp_port,
                    "user": args.smtp_user,
                    "password": args.smtp_pass
                }
                send_smtp_email(
                    smtp_cfg=smtp_cfg,
                    to_email=email,
                    subject=rendered["subject"],
                    body=rendered["body"],
                    sender_name=args.sender_name,
                    sender_email=args.sender_email
                )
                print(f"      ✅ Successfully sent to {email}")
                lead["status"] = "SENT"
                sent_count += 1
            except Exception as e:
                print(f"      ❌ Failed to send to {email}: {e}")

    print("\n-------------------------------------------------------")
    if args.send:
        print(f"Summary: Sent {sent_count} emails.")
    else:
        print(f"Summary: Previewed {draft_count} emails. Ready for live dispatch.")
    print("-------------------------------------------------------\n")

if __name__ == "__main__":
    main()
