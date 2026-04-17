"""
Meta Business Suite Inbox Bot
Polls the Meta Business Suite inbox, reads new messages, replies via Claude CLI.

First run:  python3 inbox_bot.py --login
Subsequent: python3 inbox_bot.py
"""

import os
import sys
import time
import json
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(__file__).parent / 'inbox_bot.log'),
    ]
)
log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────

INBOX_URL     = 'https://business.facebook.com/latest/inbox/all'
SESSION_DIR   = Path(__file__).parent / '.browser_session'
REPLIED_FILE  = Path(__file__).parent / '.replied_threads.json'
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', '45'))   # seconds between checks
CLAUDE_CLI    = os.getenv('CLAUDE_CLI_PATH', 'claude')

SYSTEM_PROMPT = """You are a friendly customer service assistant for Cannibisters,
a premium cannabis and lifestyle brand in Cape Town, South Africa.

Rules:
- Keep replies short (2-4 sentences) — this is a chat inbox
- Be warm, helpful, and professional
- If asked about order status or specific stock, say you'll check and ask for their order number
- Do not make up prices or availability you don't know
- Tone: friendly, slightly casual, South African warmth
- Never discuss anything off-topic"""


# ── Selectors (Meta Business Suite — update if UI changes) ────────────────────

SEL_CONV_LIST      = '[data-testid="mbs-thread-list"] [role="listitem"]'
SEL_CONV_LIST_ALT  = '[aria-label="Conversation list"] [role="row"]'
SEL_UNREAD_DOT     = '[data-testid="unread-indicator"], [aria-label*="unread"], [class*="unread"]'
SEL_MSG_BUBBLES    = '[data-testid="message-container"] [dir="auto"]'
SEL_MSG_ALT        = '[role="listitem"] [dir="auto"]'
SEL_INPUT          = '[contenteditable="true"][aria-label*="message" i], [contenteditable="true"][placeholder*="message" i]'
SEL_INPUT_ALT      = '[contenteditable="true"][role="textbox"]'
SEL_SEND_BTN       = '[aria-label*="Send" i][type="submit"], [data-testid="send-button"]'


# ── Claude reply ──────────────────────────────────────────────────────────────

def get_reply(customer_message: str) -> str:
    try:
        result = subprocess.run(
            [CLAUDE_CLI, '--print', '--system-prompt', SYSTEM_PROMPT, customer_message],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        log.error('Claude error: %s', result.stderr[:200])
    except subprocess.TimeoutExpired:
        log.error('Claude timed out')
    except FileNotFoundError:
        log.error('Claude CLI not found')
    return "Hi! Thanks for reaching out to Cannibisters. We'll get back to you shortly 🌿"


# ── Replied thread tracker ────────────────────────────────────────────────────

def load_replied() -> set:
    if REPLIED_FILE.exists():
        return set(json.loads(REPLIED_FILE.read_text()))
    return set()

def save_replied(replied: set):
    REPLIED_FILE.write_text(json.dumps(list(replied)))


# ── Browser helpers ───────────────────────────────────────────────────────────

def wait_for_inbox(page):
    log.info('Waiting for inbox to load...')
    try:
        page.wait_for_selector(SEL_CONV_LIST, timeout=15000)
        return SEL_CONV_LIST
    except PWTimeout:
        pass
    try:
        page.wait_for_selector(SEL_CONV_LIST_ALT, timeout=10000)
        return SEL_CONV_LIST_ALT
    except PWTimeout:
        log.warning('Could not find conversation list — Meta may have changed its UI')
        return None


def get_last_customer_message(page) -> str | None:
    for sel in [SEL_MSG_BUBBLES, SEL_MSG_ALT, '[dir="auto"]']:
        bubbles = page.query_selector_all(sel)
        if bubbles:
            texts = [b.inner_text().strip() for b in bubbles if b.inner_text().strip()]
            if texts:
                return texts[-1]
    return None


def send_reply(page, text: str) -> bool:
    input_el = None
    for sel in [SEL_INPUT, SEL_INPUT_ALT]:
        input_el = page.query_selector(sel)
        if input_el:
            break

    if not input_el:
        log.warning('Could not find message input field')
        return False

    input_el.click()
    input_el.fill('')
    input_el.type(text, delay=20)
    time.sleep(0.5)

    send_btn = page.query_selector(SEL_SEND_BTN)
    if send_btn:
        send_btn.click()
    else:
        input_el.press('Enter')

    time.sleep(1)
    log.info('Reply sent')
    return True


def get_thread_id(page) -> str:
    return page.url.split('?')[0].rstrip('/')


# ── Main loop ─────────────────────────────────────────────────────────────────

def run_bot(headless: bool = False):
    replied = load_replied()
    log.info('Starting inbox bot (poll every %ds, headless=%s)', POLL_INTERVAL, headless)

    with sync_playwright() as pw:
        browser = pw.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=headless,
            args=['--disable-blink-features=AutomationControlled'],
            viewport={'width': 1280, 'height': 900},
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        page.goto(INBOX_URL)
        log.info('Navigated to inbox')

        # Wait for login if needed
        if 'login' in page.url or 'checkpoint' in page.url:
            log.warning('Not logged in — please log in manually in the browser window')
            input('Press Enter after you have logged in...')
            page.goto(INBOX_URL)

        while True:
            try:
                page.reload()
                page.wait_for_load_state('networkidle', timeout=15000)

                conv_sel = wait_for_inbox(page)
                if not conv_sel:
                    time.sleep(POLL_INTERVAL)
                    continue

                conversations = page.query_selector_all(conv_sel)
                log.info('Found %d conversations', len(conversations))

                for conv in conversations[:10]:  # check top 10
                    # Look for unread indicator
                    unread = conv.query_selector(SEL_UNREAD_DOT)
                    if not unread:
                        continue

                    conv.click()
                    page.wait_for_load_state('networkidle', timeout=10000)
                    time.sleep(1)

                    thread_id = get_thread_id(page)
                    if thread_id in replied:
                        log.info('Already replied to %s, skipping', thread_id)
                        continue

                    last_msg = get_last_customer_message(page)
                    if not last_msg:
                        log.info('No readable message in thread %s', thread_id)
                        continue

                    log.info('New message: %s', last_msg[:80])
                    reply = get_reply(last_msg)
                    log.info('Claude reply: %s', reply[:80])

                    if send_reply(page, reply):
                        replied.add(thread_id)
                        save_replied(replied)

                    time.sleep(2)

            except PWTimeout:
                log.warning('Page timeout — will retry')
            except Exception as e:
                log.error('Error in main loop: %s', e, exc_info=True)

            log.info('Sleeping %ds before next check...', POLL_INTERVAL)
            time.sleep(POLL_INTERVAL)


# ── Login mode ────────────────────────────────────────────────────────────────

def run_login():
    """Open a visible browser for the user to log in once. Session is saved."""
    log.info('Login mode — browser will open. Log in to Meta Business Suite, then press Enter here.')
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,
            viewport={'width': 1280, 'height': 900},
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(INBOX_URL)
        input('\nBrowser is open. Log in to Meta Business Suite, navigate to the inbox,\nthen press Enter here to save the session...\n')
        browser.close()
    log.info('Session saved to %s — you can now run the bot without --login', SESSION_DIR)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Meta Business Suite inbox bot')
    parser.add_argument('--login',    action='store_true', help='Open browser to log in and save session')
    parser.add_argument('--headless', action='store_true', help='Run browser headlessly (after login)')
    args = parser.parse_args()

    if args.login:
        run_login()
    else:
        run_bot(headless=args.headless)
