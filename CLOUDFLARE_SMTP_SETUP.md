# How to Set Up Outbound SMTP on Cloudflare for Xclusive Tech

Since your website and domain (`xclusivetech.co.ke`) are hosted on **Cloudflare**, Cloudflare manages your DNS records. Cloudflare does not provide an outbound SMTP sending server by itself (it only forwards incoming emails).

Here are the 3 simplest ways to get outbound SMTP working to send your cold outreach campaigns:

---

### Option 1: Resend or Brevo (Free & Recommended — 3 Minutes)

Both services give you free SMTP sending for your custom domain (`hello@xclusivetech.co.ke`).

#### Step-by-Step Setup:
1. **Create a free account** at [Resend.com](https://resend.com) (free 3,000 emails/month) or [Brevo.com](https://brevo.com) (free 300 emails/day).
2. **Add your domain**: Enter `xclusivetech.co.ke`.
3. **Add 3 DNS Records in Cloudflare Dashboard**:
   Go to your Cloudflare Dashboard -> **DNS** -> **Records** -> **Add record**:

   - **SPF Record (TXT)**:
     - **Name**: `@`
     - **Content**: `v=spf1 include:resend.com ~all` (or Brevo equivalent)
     - **TTL**: Auto
   
   - **DKIM Record (TXT)**:
     - **Name**: `resend._domainkey` (provided in your dashboard)
     - **Content**: (paste the key string provided in your dashboard)
     - **TTL**: Auto

   - **DMARC Record (TXT)**:
     - **Name**: `_dmarc`
     - **Content**: `v=DMARC1; p=none; rua=mailto:hello@xclusivetech.co.ke;`
     - **TTL**: Auto

4. **Generate SMTP Credentials**:
   - In Resend/Brevo, go to **API Keys / SMTP Settings**.
   - Note down:
     - **Host**: `smtp.resend.com` (or `smtp-relay.brevo.com`)
     - **Port**: `587`
     - **Username**: `resend` (or your Brevo account email)
     - **Password**: `your_api_key`

---

### Option 2: Send Using Google Workspace or Gmail App Password

If you already use a Gmail / Google Workspace account:

1. Go to your Google Account -> **Security** -> **2-Step Verification**.
2. Scroll to the bottom and select **App Passwords**.
3. Create an app password named `"Xclusive Outreach"`.
4. Copy the generated 16-character password (e.g. `abcd efgh ijkl mnop`).
5. Your SMTP details:
   - **Host**: `smtp.gmail.com`
   - **Port**: `587`
   - **Username**: `your_email@gmail.com`
   - **Password**: `your_16_character_app_password`

---

### Running the Outbound Engine Once SMTP is Ready

Once you have your SMTP credentials, run:

```bash
python3 scripts/outreach_engine.py \
  --csv scripts/leads_sample.csv \
  --send \
  --smtp-host "smtp.resend.com" \
  --smtp-port 587 \
  --smtp-user "resend" \
  --smtp-pass "re_YOUR_API_KEY_HERE" \
  --sender-email "hello@xclusivetech.co.ke" \
  --sender-name "Samuel Kidemi | Xclusive Tech"
```
