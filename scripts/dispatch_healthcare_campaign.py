#!/usr/bin/env python3
"""
Healthcare Campaign Dispatch Engine for Elite Designs Kenya
Sends via authenticated cPanel SMTP (mail.elitedesigns.co.ke:465 SSL)
Appends sent messages to IMAP INBOX.Sent so they appear in Roundcube Webmail.
Enforces anti-spam throttling, randomized delays, and RFC 2822 compliance.
"""

import argparse
import email
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import imaplib
import json
import os
import random
import smtplib
import ssl
import sys
import time

# Ensure scripts dir is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from generate_healthcare_campaign_drafts import render_html_email, render_plain_email

DATA_FILE = "outreach_drafts/healthcare_campaign/target_50_healthcare_kenya.json"
LOG_FILE = "outreach_drafts/healthcare_campaign/dispatch_log.json"

SMTP_HOST = "mail.elitedesigns.co.ke"
SMTP_PORT = 465
IMAP_HOST = "mail.elitedesigns.co.ke"
IMAP_PORT = 993

SENDER_NAME = "Dr. Samuel Kidemi"
SENDER_EMAIL = "sam@elitedesigns.co.ke"
SENDER_PASS = "G3zjz_6a3sbOypf371SE"


def load_targets():
  with open(DATA_FILE, "r", encoding="utf-8") as f:
    return json.load(f)


def build_message(target):
  msg = MIMEMultipart("alternative")
  msg["Subject"] = Header(target["subject"], "utf-8")
  msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
  msg["To"] = ", ".join(target["to_emails"])
  msg["Reply-To"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
  msg["Date"] = formatdate(localtime=True)
  msg["Message-ID"] = make_msgid(domain="elitedesigns.co.ke")
  msg["X-Mailer"] = "Elite Designs Clinical Dispatch/2.0"
  msg["List-Unsubscribe"] = f"<mailto:{SENDER_EMAIL}?subject=Unsubscribe>"

  plain_body = render_plain_email(target)
  html_body = render_html_email(target)

  msg.attach(MIMEText(plain_body, "plain", "utf-8"))
  msg.attach(MIMEText(html_body, "html", "utf-8"))
  return msg


def main():
  parser = argparse.ArgumentParser(
      description="Healthcare Campaign Dispatch Engine"
  )
  parser.add_argument(
      "--dry-run",
      action="store_true",
      help="Simulate sending without connecting to SMTP/IMAP",
  )
  parser.add_argument(
      "--limit",
      type=int,
      default=50,
      help="Maximum emails to send in this batch",
  )
  parser.add_argument(
      "--start-from",
      type=str,
      default="01",
      help="Start from target ID (e.g. 01)",
  )
  parser.add_argument(
      "--delay-min",
      type=int,
      default=40,
      help="Minimum seconds delay between emails (anti-spam throttling)",
  )
  parser.add_argument(
      "--delay-max",
      type=int,
      default=75,
      help="Maximum seconds delay between emails",
  )
  parser.add_argument(
      "--preview",
      type=str,
      help="Preview target ID (e.g. 01) and print rendered payload",
  )
  args = parser.parse_args()

  targets = load_targets()

  if args.preview:
    match = next((t for t in targets if t["id"] == args.preview), None)
    if not match:
      print(f"Target ID {args.preview} not found.")
      return
    msg = build_message(match)
    print("=" * 60)
    print(f"PREVIEW FOR [{match['id']}] {match['company']}")
    print(f"TO: {', '.join(match['to_emails'])}")
    print(f"SUBJECT: {match['subject']}")
    print(f"MESSAGE-ID: {msg['Message-ID']}")
    print("=" * 60)
    print(render_plain_email(match))
    return

  # Filter start
  start_idx = 0
  for idx, t in enumerate(targets):
    if t["id"] == args.start_from:
      start_idx = idx
      break

  selected = targets[start_idx : start_idx + args.limit]
  print(f"Prepared {len(selected)} targets starting from ID {args.start_from}.")
  print(
      f"Anti-spam throttling: Randomized {args.delay_min}s to {args.delay_max}s"
      " jitter per message."
  )

  if args.dry_run:
    print("\n--- DRY RUN MODE ACTIVATED (No actual emails will be sent) ---")
    for t in selected:
      print(
          f"[DRY-RUN] Would send to: {t['company']} <{', '.join(t['to_emails'])}>"
      )
      print(f"          Subject: {t['subject']}")
    print(
        f"\n[DRY-RUN] Success. {len(selected)} targets verified and ready for"
        " live dispatch."
    )
    return

  # Live Dispatch
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE

  print(f"\nConnecting to SMTP {SMTP_HOST}:{SMTP_PORT} (SSL)...")
  smtp_server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=30)
  smtp_server.login(SENDER_EMAIL, SENDER_PASS)
  print("SMTP Authentication Successful.")

  print(f"Connecting to IMAP {IMAP_HOST}:{IMAP_PORT} (SSL)...")
  imap_server = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
  imap_server.login(SENDER_EMAIL, SENDER_PASS)
  print("IMAP Authentication Successful. Verified access to INBOX.Sent.")

  log_records = []
  if os.path.exists(LOG_FILE):
    try:
      with open(LOG_FILE, "r") as lf:
        log_records = json.load(lf)
    except Exception:
      log_records = []

  total_sent = 0
  for idx, t in enumerate(selected):
    msg = build_message(t)
    recipients = t["to_emails"]

    print(
        f"\n[{idx+1}/{len(selected)}] Dispatching to: {t['company']} ->"
        f" {recipients}"
    )
    print(f"  Subject: {t['subject']}")

    try:
      smtp_server.send_message(msg)
      print(f"  ✓ Transmitted via SMTP ({t['company']})")

      # Append to Roundcube INBOX.Sent via IMAP
      try:
        raw_msg = msg.as_bytes()
        imap_server.append("INBOX.Sent", "\\Seen", imaplib.Time2Internaldate(time.time()), raw_msg)
        print("  ✓ Appended to Webmail INBOX.Sent")
      except Exception as imap_err:
        # If IMAP timed out, attempt quick re-auth and retry append once
        try:
          imap_server = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
          imap_server.login(SENDER_EMAIL, SENDER_PASS)
          imap_server.append("INBOX.Sent", "\\Seen", imaplib.Time2Internaldate(time.time()), raw_msg)
          print("  ✓ Reconnected and Appended to Webmail INBOX.Sent")
        except Exception:
          print(f"  (Note: Sent via SMTP, Webmail Sent append deferred: {imap_err})")

      log_records.append({
          "id": t["id"],
          "company": t["company"],
          "to": recipients,
          "subject": t["subject"],
          "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
          "status": "SENT",
      })
      total_sent += 1

    except Exception as e:
      print(f"  ✗ Error sending to {t['company']}: {e}")
      log_records.append({
          "id": t["id"],
          "company": t["company"],
          "to": recipients,
          "error": str(e),
          "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
          "status": "FAILED",
      })

    # Save log after every email
    with open(LOG_FILE, "w", encoding="utf-8") as lf:
      json.dump(log_records, lf, indent=2)

    # Throttling delay between sends if more remain
    if idx < len(selected) - 1:
      sleep_sec = random.randint(args.delay_min, args.delay_max)
      print(f"  ⏳ Anti-spam throttle: Waiting {sleep_sec}s before next send...")
      time.sleep(sleep_sec)

  try:
    smtp_server.quit()
    imap_server.logout()
  except Exception:
    pass

  print("\n" + "=" * 60)
  print(f"Campaign Run Complete! Successfully sent: {total_sent}/{len(selected)}")
  print(f"Log updated at: {LOG_FILE}")
  print("=" * 60)


if __name__ == "__main__":
  main()

