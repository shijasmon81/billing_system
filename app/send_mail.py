import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_invoice_email(customer_email: str, invoice_html: str):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # Use App Password, not your real password

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Invoice"
    msg["From"] = sender_email
    msg["To"] = customer_email

    html_part = MIMEText(invoice_html, "html")
    msg.attach(html_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, customer_email, msg.as_string())

    print(f"Invoice sent to {customer_email}")
