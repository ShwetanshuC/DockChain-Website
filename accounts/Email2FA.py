import smtplib
import ssl
from email.message import EmailMessage

# === CONFIGURE THESE ===
EMAIL_SENDER = "aadarsh.jena2008@gmail.com"
EMAIL_PASSWORD = "your_app_specific_password"  # Do NOT use your main Gmail password!
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port

def send_password_change_email(to_email, username):
    subject = "Password Change Attempt Notification"
    body = f"""\
Hi {username},

We noticed an attempt to change your password. If this was you, please continue the process.
If not, please secure your account immediately.

Thanks,
Your Web App Team"""

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Send the email using SMTP over SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f"[✔] Password change email sent to {to_email}")