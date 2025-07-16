import smtplib
import ssl
from email.message import EmailMessage

# === Configuration ===
EMAIL_SENDER = "dockchainverify@gmail.com"              # Your Gmail address
EMAIL_PASSWORD = "aslmngqjsuytsovg"       # App password (not your regular Gmail password)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port

def send_password_email(to_email, code):
    # Create the email message
    msg = EmailMessage()
    msg["Subject"] = "Change Your Password"
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    # HTML email body with a link
    #link_url = "http://127.0.0.1:8000/admin/password_change/"
    html_body = f"""
    <html>
      <body>
        <p>Hi,</p>
        <p>Your 6-digit verification code is:</p>
        <h2 style="letter-spacing: 4px; font-size: 24px;">{code}</h2>
        <p>This code will expire in 10 minutes.</p>
      </body>
    </html>
    """

    # Add plain text fallback and HTML version
    #msg.set_content("To change your password, visit: " + link_url)
    msg.add_alternative(html_body, subtype="html")

    # Connect and send email using SMTP with SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f"[✔] Email sent successfully to {to_email}")
