# Xclusive Tech enquiries

Standalone Worker route `/api/leads*` runs alongside the existing Pages site. D1 commits the enquiry and notification outbox together before acknowledging a submission. Email uses the existing verified owner destination; inbound `hello@` routing is unchanged.

Secrets: `NOTIFICATION_TO` (verified existing forwarding destination), `IP_HASH_KEY` (random private HMAC key). Keep these in Cloudflare secrets, never source control. `send_email` allows only the site's sender. The destination is never accepted from browser input.

Retry cron runs every five minutes with exponential backoff. Notification delivery is at least once: an interruption after email acceptance and before the database update can repeat an email. Stored enquiries remain authoritative. A successful API response confirms durable storage, not that Gmail placed mail in the inbox.

Operations (authenticated Wrangler, config `cloudflare/leads/wrangler.jsonc`):

- Health: `GET https://www.xclusivetech.co.ke/api/leads/health`
- Review pending notifications: `wrangler d1 execute xclusivetech-leads --remote --command "SELECT lead_id,state,attempts,last_error FROM lead_notifications WHERE state!='sent'" -c cloudflare/leads/wrangler.jsonc`
- Enquiry records can be reviewed in the authenticated Cloudflare D1 console, `xclusivetech-leads` database, `leads` table. There is no public reader or admin endpoint.
- Apply migrations: `wrangler d1 migrations apply xclusivetech-leads --remote -c cloudflare/leads/wrangler.jsonc`
- Deploy: `wrangler deploy -c cloudflare/leads/wrangler.jsonc`
- Tests (Node 22.13+): `node --test cloudflare/leads/test/service.test.mjs`
- Browser checks, local server port 8766: `python scripts/test_cloudflare_forms.py`

Privacy: no raw IP addresses or enquiry contents in logs/analytics. Rate-limit keys are HMACs with short-lived buckets. Enquiry retention follows the published privacy policy; operators must review/delete expired records and action deletion requests in D1 and the destination mailbox. No automatic deletion of unsent leads is performed.

Native HTML forms remain usable without JavaScript. On server failure, the visitor receives an explicit error and can return to retry or contact WhatsApp. JavaScript keeps entered fields on failed requests. Newsletter requests are stored as email-only opt-ins, not automatically added to a marketing platform.

## Printing artwork

`POST /api/leads/artwork` accepts a single binary PDF, PNG or JPG up to 10 MiB from the configured site origins. File signatures and types are checked; this is not a malware scan or an automatic preflight check. Per-IP upload limits use the existing hashed rate buckets. A signed receipt is returned only after storage succeeds.

Small artwork uploads use the private `PRINT_ARTWORK` KV namespace with automatic 30-day expiry. R2 is not enabled on this account; no R2 subscription or paid plan was activated. For files over 10 MiB or source-design packages, the form accepts an artwork link instead. Capacity limits return an explicit error with the link/WhatsApp alternative.

The enquiry endpoint verifies the signed artwork receipt and appends a private, expiring download link to the stored enquiry and owner notification. Downloads require an unguessable signed capability and force attachment delivery; there is no public file listing. KV can take up to a minute to become available in another region, so missing/new objects return a retry response rather than a false permanent-not-found result. Keep download links private. Expired artwork can be shared again by the sender.
