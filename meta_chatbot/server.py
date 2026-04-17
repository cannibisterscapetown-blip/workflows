import os
import json
import hashlib
import hmac
import logging
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from claude_handler import get_claude_reply

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('META_VERIFY_TOKEN', 'cannibisters_chatbot_verify')
APP_SECRET   = os.getenv('META_APP_SECRET', '')
API_VERSION  = 'v21.0'
GRAPH_URL    = f'https://graph.facebook.com/{API_VERSION}'

INSTAGRAM_ID = os.getenv('INSTAGRAM_ID', '17841459113832751')


# ── Webhook verification (GET) ────────────────────────────────────────────────

@app.route('/webhook', methods=['GET'])
def verify():
    mode      = request.args.get('hub.mode')
    token     = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        log.info('Webhook verified successfully')
        return challenge, 200
    log.warning('Webhook verification failed')
    return 'Forbidden', 403


# ── Incoming events (POST) ────────────────────────────────────────────────────

@app.route('/webhook', methods=['POST'])
def handle_event():
    if APP_SECRET:
        _verify_signature(request)

    body = request.get_json(silent=True) or {}
    log.info('Incoming payload: %s', json.dumps(body, indent=2))

    object_type = body.get('object')

    if object_type == 'page':
        for entry in body.get('entry', []):
            for msg_event in entry.get('messaging', []):
                _handle_messenger(msg_event)

    elif object_type == 'instagram':
        for entry in body.get('entry', []):
            for msg_event in entry.get('messaging', []):
                _handle_instagram(msg_event)

    return jsonify({'status': 'ok'}), 200


# ── Platform handlers ─────────────────────────────────────────────────────────

def _handle_messenger(event):
    sender_id = event.get('sender', {}).get('id')
    msg = event.get('message', {})
    text = msg.get('text', '').strip()

    if not text or msg.get('is_echo'):
        return

    log.info('Messenger message from %s: %s', sender_id, text)
    reply = get_claude_reply(text, platform='Facebook Messenger')
    _send_messenger_reply(sender_id, reply)


def _handle_instagram(event):
    sender_id = event.get('sender', {}).get('id')
    msg = event.get('message', {})
    text = msg.get('text', '').strip()

    if not text or msg.get('is_echo'):
        return

    log.info('Instagram DM from %s: %s', sender_id, text)
    reply = get_claude_reply(text, platform='Instagram')
    _send_instagram_reply(sender_id, reply)


# ── Send helpers ──────────────────────────────────────────────────────────────

def _send_messenger_reply(recipient_id, text):
    url = f'{GRAPH_URL}/me/messages'
    payload = {
        'recipient': {'id': recipient_id},
        'message':   {'text': text},
        'messaging_type': 'RESPONSE',
    }
    resp = requests.post(url, json=payload, params={'access_token': ACCESS_TOKEN})
    if not resp.ok:
        log.error('Messenger send failed: %s', resp.text)
    else:
        log.info('Messenger reply sent to %s', recipient_id)


def _send_instagram_reply(recipient_id, text):
    url = f'{GRAPH_URL}/{INSTAGRAM_ID}/messages'
    payload = {
        'recipient': {'id': recipient_id},
        'message':   {'text': text},
        'messaging_type': 'RESPONSE',
    }
    resp = requests.post(url, json=payload, params={'access_token': ACCESS_TOKEN})
    if not resp.ok:
        log.error('Instagram send failed: %s', resp.text)
    else:
        log.info('Instagram reply sent to %s', recipient_id)


# ── Signature verification ────────────────────────────────────────────────────

def _verify_signature(req):
    sig_header = req.headers.get('X-Hub-Signature-256', '')
    if not sig_header.startswith('sha256='):
        return
    expected = hmac.new(APP_SECRET.encode(), req.data, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig_header[7:], expected):
        log.warning('Invalid webhook signature')


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    log.info('Starting Meta chatbot server on port %d', port)
    app.run(host='0.0.0.0', port=port, debug=False)
