# Xclusive Tech — Outbound Sales, Lead Prospecting & Call Booking Playbook

This playbook provides an end-to-end outbound client acquisition system tailored specifically for **Xclusive Tech** (Web Design, Daraja M-Pesa E-Commerce, Custom Software & Frostwood CRM).

---

## 1. High-Value Target Niches (ICP Matrix)

| Target Vertical | Prime Pain Point | Winning Hook | Primary Offer | Ticket Size (KES) |
|---|---|---|---|---|
| **High-Ticket Tour & Safari Operators** (Nairobi, Mombasa, Arusha) | Slow mobile sites, dated booking forms, no instant card/M-Pesa deposits. | "Trimmed load time from 4s to 1.2s; automated direct deposits like Santorini Queen & Diani Elite." | Custom Tourism Web Architecture | KES 49,000 – 85,000 |
| **Active Instagram / TikTok Retail Brands** | Manual DM selling, chasing Till payments, lost midnight orders. | "Turn DM inquiries into 10-second automated Daraja M-Pesa STK push checkouts." | E-Commerce Pro Package | KES 72,000 – 85,000 |
| **Professional Firms** (Law, Health Clinics, Real Estate, Consulting) | Outdated WordPress/Wix sites, no local SEO, zero mobile optimization. | "Rank #1 in Kilimani/Westlands + WhatsApp booking engine." | Starter or Business Growth Site | KES 25,000 – 62,000 |
| **B2B Agencies & Contractors** | Leads lost across WhatsApp chats, manual PDF invoicing. | "Frostwood CRM: Unified pipeline + M-Pesa STK push invoicing." | Frostwood CRM + Implementation | KES 15,000 – 45,000+ |

---

## 2. Lead Sourcing Blueprint (How to Get 100 Verified Leads/Day)

### Method A: Meta Ad Library (High Intent & Ready Budget)
Companies running paid ads already have a marketing budget:
1. Go to [Meta Ad Library](https://www.facebook.com/ads/library/).
2. Select Location: **Kenya**, Category: **All Ads**.
3. Search keywords: `"safari"`, `"boutique"`, `"furniture"`, `"clinic"`, `"law firm"`.
4. Check where their ad links:
   - If it links to a slow website or directly to WhatsApp, they urgently need an **Express Sales Landing Page (KES 15k)** or **E-Commerce Store (KES 72k+)**.

### Method B: Google Maps & Local Search
1. Search on Google Maps:
   - `"tour companies Nairobi"`
   - `"boutiques Westlands"`
   - `"real estate agents Kilimani"`
   - `"dental clinic Nairobi"`
2. Check their website URL:
   - Run our audit tool: `python3 scripts/audit_prospect_site.py <their-url>`
   - If mobile load speed > 3 seconds, or missing SSL, or outdated design, add them to `scripts/leads_sample.csv`.

### Method C: Finding Verified Email Addresses
1. Check the website's Contact page or footer.
2. Use free tools like **Hunter.io** or **Anymail Finder** on their domain.
3. Google Dork: `site:<domain.co.ke> "@" OR email OR info OR contact`

---

## 3. The 3-Touch Cold Outreach Sequence

### Touch 1: The Observation & Pain Point (Day 1)
*Automated by `scripts/outreach_engine.py`*
- Focuses on a genuine observation (mobile speed, manual DM sales, or local SEO).
- Introduces social proof (Top Digitally Fit Web Design Firm of the Year, 120+ client websites).
- Low friction CTA: A 10-minute discovery call or free 3-point conversion audit.

### Touch 2: Value Add & Case Study (Day 3)
```text
Subject: Re: [Previous Subject]

Hi {contact_name},

Following up briefly on my note from Tuesday.

I recorded a quick 60-second video breakdown showing how streamlining mobile checkout speed on Safaricom 4G increased conversion rates for Kenyan brands we work with (like Santorini Queen & Diani Elite).

Would you be open to a 10-minute chat this Thursday at 11 AM or 2 PM EAT?

👉 Book on WhatsApp: https://wa.me/254722753819?text=Hi%20Samuel,%20ready%20for%20our%20call.

Best,
Samuel Kidemi | Xclusive Tech
```

### Touch 3: The "Breakup" & Permission to Close (Day 7)
```text
Subject: Should I close your file, {contact_name}?

Hi {contact_name},

I haven't heard back, so I assume upgrading {website}'s mobile performance and booking flow isn't a priority right now—totally understand.

If things change or you ever want to automate your M-Pesa checkouts or refresh your digital presence, feel free to reach out anytime on WhatsApp: +254 722 753 819.

Wishing {company_name} continued success!

Best regards,
Samuel Kidemi
```

---

## 4. Multi-Channel Acceleration (The WhatsApp Touch)

In Kenya, WhatsApp has the highest engagement rate. Once an email is sent:
Send a polite, 2-line WhatsApp note from `+254722753819`:

> *"Hi {contact_name}, Samuel here from Xclusive Tech. I just sent a quick email regarding {website}'s mobile booking speed. Thought I'd drop a quick note here in case WhatsApp is easier. Let me know if you'd like a quick 5-min chat!"*

---

## 5. Running the Automated Engine

### Step 1: Add New Prospects
Edit or append to `scripts/leads_sample.csv` or create your own `leads.csv`:
```csv
company_name,contact_name,email,phone,niche,website,personalized_observation,status,notes
```

### Step 2: Audit Prospect Websites Live
```bash
python3 scripts/audit_prospect_site.py example.co.ke
```

### Step 3: Preview & Generate Drafts
```bash
python3 scripts/outreach_engine.py --csv scripts/leads_sample.csv --dry-run --save-drafts
```

### Step 4: Dispatch via SMTP (Live Sending)
Using Google Workspace / Gmail App Password or cPanel SMTP:
```bash
python3 scripts/outreach_engine.py \
  --csv scripts/leads_sample.csv \
  --send \
  --smtp-host "smtp.gmail.com" \
  --smtp-port 587 \
  --smtp-user "hello@xclusivetech.co.ke" \
  --smtp-pass "YOUR_APP_PASSWORD" \
  --booking-link "https://wa.me/254722753819?text=Hi%20Samuel,%20let%27s%20book%20a%20call"
```
