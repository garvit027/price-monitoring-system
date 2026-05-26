import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from app.services.email import send_price_alert_email, send_tracking_started_email

# Send to the user's primary email address
recipient = "garvitjuneja27@gmail.com"

print(f"Testing SMTP Configuration...")
print(f"Using SMTP_USERNAME: {os.getenv('SMTP_USERNAME')}")

try:
    print("1. Sending 'Tracking Started' Email...")
    send_tracking_started_email(
        product_name="Apple iPhone 15 Pro (Black Titanium, 128 GB)",
        product_url="https://www.flipkart.com/apple-iphone-15-pro-black-titanium-128-gb/p/itm283311e51b143",
        current_price=109900.0,
        currency_symbol="₹",
        recipient_email=recipient
    )

    print("2. Sending 'Price Drop Alert' Email...")
    send_price_alert_email(
        product_name="Apple iPhone 15 Pro (Black Titanium, 128 GB)",
        product_url="https://www.flipkart.com/apple-iphone-15-pro-black-titanium-128-gb/p/itm283311e51b143",
        new_price=104900.0,
        target_price=105000.0,
        currency_symbol="₹",
        recipient_email=recipient
    )
    print(f"Emails sent successfully to {recipient}!")
except Exception as e:
    print(f"Failed to send email: {e}")
