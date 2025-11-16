import smtplib
from email.mime.text import MIMEText
import requests

# -----------------------------
# SLACK ALERT FUNCTION
# -----------------------------
def send_slack_alert(webhook_url, message):
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("[ALERT] Slack message sent")
        else:
            print("[ALERT ERROR] Slack failed:", response.text)
    except Exception as e:
        print("[ALERT ERROR] Slack exception:", e)


# -----------------------------
# EMAIL ALERT FUNCTION (GMAIL)
# -----------------------------
def send_email_alert(sender_email, app_password, receiver_email, subject, body):
    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("[ALERT] Email sent successfully")
    except Exception as e:
        print("[ALERT ERROR] Email failed:", e)
