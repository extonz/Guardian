"""
Módulo de notificaciones: Telegram y Discord (webhook).
Provee configuraciones y funciones para enviar mensajes.
"""

import requests
from typing import Tuple
from src.utils.settings_manager import load_settings, save_settings


def setup_telegram(bot_token: str, chat_id: str) -> Tuple[bool, str]:
    settings = load_settings()
    if 'notifications' not in settings:
        settings['notifications'] = {}
    settings['notifications']['telegram'] = {
        'enabled': True,
        'bot_token': bot_token,
        'chat_id': chat_id
    }
    save_settings(settings)
    return True, "Telegram configurado"


def setup_discord(webhook_url: str) -> Tuple[bool, str]:
    settings = load_settings()
    if 'notifications' not in settings:
        settings['notifications'] = {}
    settings['notifications']['discord'] = {
        'enabled': True,
        'webhook_url': webhook_url
    }
    save_settings(settings)
    return True, "Discord configurado"


def send_telegram_message(message: str, timeout: int = 5) -> Tuple[bool, str]:
    settings = load_settings()
    telegram = settings.get('notifications', {}).get('telegram', {})
    if not telegram.get('enabled'):
        return False, "Telegram no configurado"
    try:
        url = f"https://api.telegram.org/bot{telegram['bot_token']}/sendMessage"
        payload = {'chat_id': telegram['chat_id'], 'text': message}
        r = requests.post(url, json=payload, timeout=timeout)
        return (r.status_code == 200, f"HTTP {r.status_code}")
    except Exception as e:
        return False, str(e)


def send_discord_message(message: str, title: str = "Guardian Alert", timeout: int = 5) -> Tuple[bool, str]:
    settings = load_settings()
    discord = settings.get('notifications', {}).get('discord', {})
    if not discord.get('enabled'):
        return False, "Discord no configurado"
    try:
        payload = {
            'embeds': [{
                'title': title,
                'description': message,
                'color': 3498598
            }]
        }
        r = requests.post(discord['webhook_url'], json=payload, timeout=timeout)
        return (r.status_code in (200, 204), f"HTTP {r.status_code}")
    except Exception as e:
        return False, str(e)
