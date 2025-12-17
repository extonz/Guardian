# whitelist.py
ALLOWED_DOMAINS = [
    {"domain": "classroom.google.com", "type": "exact"},
    {"domain": "moodle.org", "type": "subdomain"},
    {"domain": "khanacademy.org", "type": "subdomain"},
    {"domain": "scratch.mit.edu", "type": "exact"},
    {"domain": "code.org", "type": "exact"},
    {"domain": "duolingo.com", "type": "exact"},
    {"domain": "edx.org", "type": "subdomain"},
    {"domain": "coursera.org", "type": "subdomain"},
    {"domain": "miriadax.net", "type": "subdomain"},
    {"domain": "geogebra.org", "type": "subdomain"},
    {"domain": "openstax.org", "type": "subdomain"},
    {"domain": "phet.colorado.edu", "type": "exact"},
    {"domain": "wikipedia.org", "type": "subdomain"},
    {"domain": "wiktionary.org", "type": "subdomain"},
    {"domain": "wikibooks.org", "type": "subdomain"},
    {"domain": "wikiversity.org", "type": "subdomain"},
    {"domain": "britannica.com", "type": "exact"},
    {"domain": "rae.es", "type": "exact"},
    {"domain": "dle.rae.es", "type": "exact"},
    {"domain": "wordreference.com", "type": "exact"},
    {"domain": "dictionary.cambridge.org", "type": "exact"},
    {"domain": "lexico.com", "type": "exact"},
    {"domain": "scholar.google.com", "type": "exact"},
    {"domain": "books.google.com", "type": "exact"},
    {"domain": "wolframalpha.com", "type": "exact"},
    {"domain": "eric.ed.gov", "type": "exact"},
    {"domain": "education.iseek.com", "type": "exact"},
    {"domain": "infotopia.info", "type": "exact"},
    {"domain": "virtuallrc.com", "type": "exact"},
    {"domain": "worldwidescience.org", "type": "exact"},
    {"domain": "science.gov", "type": "exact"},
    {"domain": "refseek.com", "type": "exact"},
    {"domain": "base-search.net", "type": "exact"},
    {"domain": "openlibrary.org", "type": "exact"},
    {"domain": "ncbi.nlm.nih.gov", "type": "subdomain"},
    {"domain": "pubmed.ncbi.nlm.nih.gov", "type": "exact"},
    {"domain": "educacionyfp.gob.es", "type": "subdomain"},
    {"domain": "educacion.gob.es", "type": "subdomain"},
    {"domain": "mecd.gob.es", "type": "subdomain"},
    {"domain": "edu.xunta.es", "type": "subdomain"},
    {"domain": "centros.edu.xunta.gal/iesleliadoura", "type": "exact"},
    {"domain": "educalab.es", "type": "exact"},
    {"domain": "kiddle.co", "type": "exact"}
]

# ===== NOTIFICACIONES AVANZADAS =====
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.settings_manager import load_settings, save_settings
from datetime import datetime

def setup_telegram(bot_token, chat_id):
    """Configura integraciÃ³n con Telegram."""
    settings = load_settings()
    if 'notifications' not in settings:
        settings['notifications'] = {}
    
    settings['notifications']['telegram'] = {
        'enabled': True,
        'bot_token': bot_token,
        'chat_id': chat_id
    }
    save_settings(settings)

def send_telegram_message(message):
    """EnvÃ­a mensaje por Telegram."""
    settings = load_settings()
    telegram = settings.get('notifications', {}).get('telegram', {})
    
    if not telegram.get('enabled'):
        return False, "Telegram no configurado"
    
    try:
        url = f"https://api.telegram.org/bot{telegram['bot_token']}/sendMessage"
        payload = {
            'chat_id': telegram['chat_id'],
            'text': message
        }
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200, "Mensaje enviado"
    except Exception as e:
        return False, str(e)

def setup_discord(webhook_url):
    """Configura integraciÃ³n con Discord."""
    settings = load_settings()
    if 'notifications' not in settings:
        settings['notifications'] = {}
    
    settings['notifications']['discord'] = {
        'enabled': True,
        'webhook_url': webhook_url
    }
    save_settings(settings)

def send_discord_message(message, title="Guardian Alert"):
    """EnvÃ­a mensaje por Discord."""
    settings = load_settings()
    discord = settings.get('notifications', {}).get('discord', {})
    
    if not discord.get('enabled'):
        return False, "Discord no configurado"
    
    try:
        payload = {
            'embeds': [{
                'title': title,
                'description': message,
                'color': 3498598,
                'footer': {'text': 'Guardian Anti-Distraction'}
            }]
        }
        response = requests.post(discord['webhook_url'], json=payload, timeout=5)
        return response.status_code in [200, 204], "Enviado a Discord"
    except Exception as e:
        return False, str(e)

