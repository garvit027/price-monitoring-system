import asyncio

async def send_notification(message):
    try:
        print(f"🔔 Sending notification: {message}")

        # simulate API call delay
        await asyncio.sleep(1)

        print("✅ Notification sent")

    except Exception as e:
        print(f"❌ Notification failed: {e}")