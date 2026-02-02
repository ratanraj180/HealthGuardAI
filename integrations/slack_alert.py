import requests
from config.settings import SLACK_WEBHOOK_URL

def send_slack_alert(message):
    try:
        if "FAKE" in SLACK_WEBHOOK_URL:
            # Don't actually send if it's the default fake URL
            # print(f"[MOCK SLACK] {message}") 
            return
            
        payload = {"text": message}
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")
