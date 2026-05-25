import os
import requests
import logging

logger = logging.getLogger(__name__)

def send_telegram_alert(chat_id: str, product_name: str, product_url: str, new_price: float, target_price: float, currency_symbol: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.warning("Telegram Bot Token is missing. Skipping Telegram notification.")
        return
        
    message = (
        f"🚨 *PRICE DROP ALERT* 🚨\n\n"
        f"*{product_name}*\nhas dropped to {currency_symbol}{new_price}!\n"
        f"(Your target was {currency_symbol}{target_price})\n\n"
        f"Buy it now: {product_url}"
    )
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info(f"Telegram alert sent to {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send Telegram message to {chat_id}: {e}")
