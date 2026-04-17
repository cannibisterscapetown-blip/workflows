import os
import subprocess
import logging

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a friendly and knowledgeable customer service assistant for Cannibisters,
a premium cannabis and lifestyle brand based in Cape Town, South Africa.

Your role:
- Answer customer questions about products, orders, and the brand
- Be warm, helpful, and professional
- Keep replies concise (2-4 sentences max) — these are chat messages
- If you don't know something specific (like a live order status), politely ask them to
  contact the team directly or visit the website
- Do not make up prices or product details you're unsure about
- Tone: friendly, slightly casual, South African warmth

Never discuss anything unrelated to the brand or customer service."""

CLAUDE_CLI = os.getenv('CLAUDE_CLI_PATH', 'claude')


def get_claude_reply(user_message: str, platform: str = 'chat') -> str:
    prompt = f"[{platform}] Customer message: {user_message}"

    try:
        result = subprocess.run(
            [CLAUDE_CLI, '--print', '--system-prompt', SYSTEM_PROMPT, prompt],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        log.error('Claude CLI error: %s', result.stderr)
    except subprocess.TimeoutExpired:
        log.error('Claude CLI timed out')
    except FileNotFoundError:
        log.error('Claude CLI not found at: %s', CLAUDE_CLI)

    return "Hi! Thanks for reaching out to Cannibisters. Our team will get back to you shortly 🌿"
