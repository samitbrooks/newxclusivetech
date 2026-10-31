PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS leads (
 id TEXT PRIMARY KEY,
 reference TEXT NOT NULL UNIQUE,
 client_request_id TEXT NOT NULL UNIQUE,
 payload_hash TEXT NOT NULL,
 name TEXT NOT NULL,
 phone TEXT NOT NULL,
 email TEXT NOT NULL DEFAULT '',
 company TEXT NOT NULL DEFAULT '',
 service TEXT NOT NULL DEFAULT '',
 budget TEXT NOT NULL DEFAULT '',
 message TEXT NOT NULL DEFAULT '',
 county TEXT NOT NULL DEFAULT '',
 form_id TEXT NOT NULL,
 page_path TEXT NOT NULL,
 created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS lead_notifications (
 lead_id TEXT PRIMARY KEY REFERENCES leads(id),
 state TEXT NOT NULL DEFAULT 'pending' CHECK(state IN ('pending','sending','sent')),
 attempts INTEGER NOT NULL DEFAULT 0,
 next_attempt_at INTEGER NOT NULL,
 locked_until INTEGER NOT NULL DEFAULT 0,
 sent_at INTEGER,
 last_error TEXT
);
CREATE INDEX IF NOT EXISTS lead_notifications_due ON lead_notifications(state,next_attempt_at,locked_until);
CREATE TABLE IF NOT EXISTS rate_buckets (
 bucket_key TEXT PRIMARY KEY,
 hits INTEGER NOT NULL,
 expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS rate_buckets_expiry ON rate_buckets(expires_at);
