import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_test_alert():
    # Email configuration - UPDATE THESE VALUES
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'sahithisuresh14@gmail.com'  # Replace with your Gmail
    sender_password = 'ajnz tydt thwr eidh'
    recipient_email = 'sahithisuresh14@gmail.com'  # Replace with recipient

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Test Churn Alert Email'

    body = """
    This is a test alert email from your Churn Prediction System.

    If you receive this, your email configuration is working!

    Customer ID: TEST001
    Churn Probability: 0.95
    Reasons: High complaints, low usage
    Action Required: Contact customer immediately

    Best regards,
    Churn Alert System
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()

        print("✅ Test email sent successfully!")
        print(f"Check {recipient_email} for the test alert.")

    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have 2FA enabled on Gmail")
        print("2. Generate App Password from https://myaccount.google.com/apppasswords")
        print("3. Use the 16-character App Password (not your regular password)")
        print("4. Update sender_email and sender_password in this script")

if __name__ == "__main__":
    send_test_alert()
