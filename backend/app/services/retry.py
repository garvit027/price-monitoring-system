import time

def retry(func, retries=3, delay=1):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            print(f"Retry {attempt+1} failed: {e}")
            time.sleep(delay)
    print("❌ All retries failed")