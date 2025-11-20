import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertAgent:
    def __init__(self, smtp_server=None, smtp_port=587, smtp_username=None, smtp_password=None, recipient_email=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.recipient_email = recipient_email

    def identify_at_risk(self, df, churn_probs, top_n=5):
        df_with_probs = df.copy()
        df_with_probs['churn_probability'] = churn_probs
        at_risk = df_with_probs.sort_values('churn_probability', ascending=False).head(top_n)
        return at_risk[['customer_id', 'churn_probability']]

    def simulate_alert_emails(self, at_risk_customers):
        alerts = []
        for _, row in at_risk_customers.iterrows():
            customer_id = row['customer_id']
            prob = row['churn_probability']
            email = f"""
Subject: High Churn Risk Alert for Customer {customer_id}

Dear Account Manager,

Customer {customer_id} has a churn probability of {prob:.2f}. Please follow up immediately to retain the customer.

Reasons: High complaints, low usage, recent tenure.

Best,
Churn Alert System
"""
            alerts.append(email.strip())
        return alerts

    def send_alert_emails(self, at_risk_customers):
        if not all([self.smtp_server, self.smtp_username, self.smtp_password, self.recipient_email]):
            print("Email configuration incomplete. Skipping real email alerts.")
            return

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)

            for _, row in at_risk_customers.iterrows():
                customer_id = row['customer_id']
                prob = row['churn_probability']

                msg = MIMEMultipart()
                msg['From'] = self.smtp_username
                msg['To'] = self.recipient_email
                msg['Subject'] = f"High Churn Risk Alert for Customer {customer_id}"

                body = f"""
Dear Account Manager,

Customer {customer_id} has a churn probability of {prob:.2f}. Please follow up immediately to retain the customer.

Reasons: High complaints, low usage, recent tenure.

Best,
Churn Alert System
"""
                msg.attach(MIMEText(body, 'plain'))

                server.sendmail(self.smtp_username, self.recipient_email, msg.as_string())
                print(f"Alert email sent for Customer {customer_id}")

            server.quit()
            print("All alert emails sent successfully.")
        except Exception as e:
            print(f"Failed to send emails: {str(e)}")
            print("Common issues:")
            print("- For Gmail: Use 'smtp.gmail.com' and generate an app password")
            print("- Check firewall/antivirus blocking SMTP")
            print("- Verify credentials and recipient email")
