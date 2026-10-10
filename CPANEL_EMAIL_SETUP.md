# Hosting hello@xclusivetech.co.ke on your cPanel Server (kenyaremotejobs)

### Server Details Identified:
- **cPanel Server IP**: `94.72.107.251`
- **Mail Hostname**: `mail.kenyaremotejobs.com` (or `mail.xclusivetech.co.ke`)
- **Webmail Port**: `2096`
- **SMTP Port**: `587` (TLS) or `465` (SSL)

---

## Step 1: Add the Domain & Email in your cPanel

1. **Log in to your cPanel** (where `kenyaremotejobs.com` is hosted).
2. **Add Domain**:
   - Go to **Domains** -> click **Create A New Domain**.
   - Enter domain name: `xclusivetech.co.ke`.
   - Uncheck *"Share document root"* (give it its own folder or leave defaults).
   - Click **Submit**.
3. **Configure Email Routing**:
   - Go to **Email Routing** (under Email section).
   - Select domain: `xclusivetech.co.ke`.
   - Choose: **Local Mail Exchanger**.
   - Click **Change**.
4. **Create the Mailbox**:
   - Go to **Email Accounts** -> click **+ Create**.
   - Select Domain: `xclusivetech.co.ke`.
   - Username: `hello`
   - Set a strong password (remember this password!).
   - Click **Create**.

---

## Step 2: Configure Cloudflare DNS for xclusivetech.co.ke

Go to your **Cloudflare Dashboard** -> Select **xclusivetech.co.ke** -> **DNS** -> **Records**:

### 1. Delete Existing Cloudflare Email Routing MX Records
Remove:
- `route1.mx.cloudflare.net`
- `route2.mx.cloudflare.net`
- `route3.mx.cloudflare.net`

### 2. Add New DNS Records:

| Type | Name | Content / Target | Priority | Proxy Status |
|---|---|---|---|---|
| **A** | `mail` | `94.72.107.251` | N/A | **DNS only (Grey Cloud)** ⚠️ *(Crucial)* |
| **MX** | `@` | `mail.xclusivetech.co.ke` | `0` (or `10`) | N/A |
| **TXT** | `@` | `v=spf1 +mx +a +ip4:94.72.107.251 ~all` | N/A | N/A |
| **TXT** | `_dmarc` | `v=DMARC1; p=none; rua=mailto:hello@xclusivetech.co.ke;` | N/A | N/A |

*(Note: In cPanel under **Email Deliverability**, find `xclusivetech.co.ke` and copy the DKIM TXT record to Cloudflare for 100% inbox delivery).*

---

## Step 3: Accessing & Using Your Email

### Webmail Access:
You can log in to check emails and compose messages at:
- **`https://94.72.107.251:2096`** or **`https://mail.kenyaremotejobs.com:2096`**
- **Username**: `hello@xclusivetech.co.ke`
- **Password**: (the password created in cPanel)

### Outbound Cold Outreach CLI Settings:
You can now run cold outreach campaigns directly using your cPanel SMTP:
```bash
python3 scripts/outreach_engine.py \
  --csv scripts/real_leads_kenya.csv \
  --send \
  --smtp-host "mail.kenyaremotejobs.com" \
  --smtp-port 587 \
  --smtp-user "hello@xclusivetech.co.ke" \
  --smtp-pass "YOUR_CPANEL_EMAIL_PASSWORD" \
  --sender-email "hello@xclusivetech.co.ke" \
  --sender-name "Samuel Kidemi | Xclusive Tech"
```
