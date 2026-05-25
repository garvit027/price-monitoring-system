import smtplib
from email.message import EmailMessage
import os
import logging

logger = logging.getLogger(__name__)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_price_alert_email(product_name: str, product_url: str, new_price: float, target_price: float, currency_symbol: str, recipient_email: str):
    """
    Sends an email notification when a product's price drops below the alert threshold.
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD or not recipient_email:
        logger.warning(f"⚠️ Email not configured or no recipient. Skipping alert for {product_name}.")
        return

    # Check for dummy values
    if "your_email" in SMTP_USERNAME or "your_app_password" in SMTP_PASSWORD:
        logger.warning(f"⚠️ Dummy credentials detected. Skipping email for {product_name}.")
        return

    try:
        msg = EmailMessage()
        
        # HTML Content for better styling
        html_content = f"""
        <html>
            <body style="font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; background-color: #09090b; color: #f8fafc; margin: 0; padding: 40px 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #121217; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.5);">
                    <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 25px; text-align: center;">
                        <h2 style="color: white; margin: 0; font-family: 'Outfit', sans-serif; font-size: 24px; letter-spacing: 0.5px;">🚨 Price Drop Alert!</h2>
                    </div>
                    <div style="padding: 35px;">
                        <h3 style="margin-top: 0; font-family: 'Outfit', sans-serif; color: #f8fafc; font-size: 20px;">Great news!</h3>
                        <p style="color: #e2e8f0; font-size: 15px; line-height: 1.6;">The product you are tracking has dropped below your target threshold.</p>
                        
                        <div style="background-color: rgba(255, 255, 255, 0.03); padding: 20px; border-left: 4px solid #6366f1; border-radius: 4px; margin: 25px 0;">
                            <strong style="color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">Product</strong><br>
                            <span style="font-size: 16px; font-weight: 500; display: inline-block; margin-top: 4px; margin-bottom: 16px;">{product_name}</span><br>
                            
                            <strong style="color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">New Price</strong><br>
                            <span style="color: #6366f1; font-weight: bold; font-size: 24px; display: inline-block; margin-top: 4px; margin-bottom: 16px;">{currency_symbol}{new_price}</span><br>
                            
                            <strong style="color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">Target Price</strong><br>
                            <span style="font-size: 16px; display: inline-block; margin-top: 4px;">{currency_symbol}{target_price}</span>
                        </div>
                        
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="margin: 40px auto 10px auto;">
                            <tr>
                                <td align="center" bgcolor="#6366f1" style="border-radius: 8px;">
                                    <a href="{product_url}" target="_blank" style="display: inline-block; padding: 14px 30px; color: #ffffff; text-decoration: none; font-weight: 600; font-size: 15px; font-family: 'Inter', sans-serif;">View Product</a>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div style="background-color: #0c0c0e; border-top: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; text-align: center; font-size: 13px; color: #94a3b8;">
                        Powered by Price Monitoring System
                    </div>
                </div>
            </body>
        </html>
        """

        msg.set_content(f"Price Drop Alert: {product_name} dropped to {currency_symbol}{new_price} (Target: {currency_symbol}{target_price}). Buy here: {product_url}")
        msg.add_alternative(html_content, subtype='html')

        msg["Subject"] = f"Price Drop Alert: {product_name}"
        msg["From"] = SMTP_USERNAME
        msg["To"] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            
        logger.info(f"📧 Email alert sent successfully for {product_name}")

    except Exception as e:
        logger.error(f"❌ Failed to send email alert for {product_name}: {e}")

def send_tracking_started_email(product_name: str, product_url: str, current_price: float, currency_symbol: str, recipient_email: str):
    """
    Sends an email confirmation when a user starts tracking a new product.
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD or not recipient_email:
        logger.warning(f"⚠️ Email not configured or no recipient. Skipping tracking confirmation for {product_name}.")
        return

    # Check for dummy values
    if "your_email" in SMTP_USERNAME or "your_app_password" in SMTP_PASSWORD:
        logger.warning(f"⚠️ Dummy credentials detected. Skipping email for {product_name}.")
        return

    try:
        msg = EmailMessage()
        
        html_content = f"""
        <html>
            <body style="font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; background-color: #09090b; color: #f8fafc; margin: 0; padding: 40px 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #121217; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.5);">
                    <div style="background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%); padding: 25px; text-align: center;">
                        <h2 style="color: white; margin: 0; font-family: 'Outfit', sans-serif; font-size: 24px; letter-spacing: 0.5px;">✅ Asset Tracking Active!</h2>
                    </div>
                    <div style="padding: 35px;">
                        <h3 style="margin-top: 0; font-family: 'Outfit', sans-serif; color: #f8fafc; font-size: 20px;">Tracking Started</h3>
                        <p style="color: #e2e8f0; font-size: 15px; line-height: 1.6;">We have successfully securely synced your asset to our monitoring network.</p>
                        
                        <div style="background-color: rgba(255, 255, 255, 0.03); padding: 20px; border-left: 4px solid #3b82f6; border-radius: 4px; margin: 25px 0;">
                            <strong style="color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">Product</strong><br>
                            <span style="font-size: 16px; font-weight: 500; display: inline-block; margin-top: 4px; margin-bottom: 16px;">{product_name}</span><br>
                            
                            <strong style="color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">Starting Price</strong><br>
                            <span style="color: #3b82f6; font-weight: bold; font-size: 24px; display: inline-block; margin-top: 4px;">{currency_symbol}{current_price}</span>
                        </div>
                        
                        <p style="color: #94a3b8; font-size: 14px; margin-top: 25px;">You can set a target threshold on the dashboard to receive notifications if the price drops.</p>
                        
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="margin: 40px auto 10px auto;">
                            <tr>
                                <td align="center" bgcolor="#3b82f6" style="border-radius: 8px;">
                                    <a href="{product_url}" target="_blank" style="display: inline-block; padding: 14px 30px; color: #ffffff; text-decoration: none; font-weight: 600; font-size: 15px; font-family: 'Inter', sans-serif;">View Origin Asset</a>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div style="background-color: #0c0c0e; border-top: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; text-align: center; font-size: 13px; color: #94a3b8;">
                        Powered by Price Monitoring System
                    </div>
                </div>
            </body>
        </html>
        """

        msg.set_content(f"Tracking Started: {product_name} is currently at {currency_symbol}{current_price}. We'll monitor it for you!")
        msg.add_alternative(html_content, subtype='html')

        msg["Subject"] = f"Tracking Started: {product_name}"
        msg["From"] = SMTP_USERNAME
        msg["To"] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            
        logger.info(f"📧 Tracking confirmation email sent successfully for {product_name}")

    except Exception as e:
        logger.error(f"❌ Failed to send tracking confirmation email for {product_name}: {e}")
