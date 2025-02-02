import os
import gspread
import smtplib
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("SheetName").sheet1
emails = sheet.col_values(1)[1:]  # Skipping header row

# Email setup
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = os.getenv("EMAIL_USER")  # Store in .env
sender_password = os.getenv("EMAIL_PASSWORD")  # Store in .env

# Create SMTP session
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    for email in emails:
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = "Invitation"
            body = "Dear recipient,\n\nYou are invited to our event.\n\nBest regards,\nYour Name"
            msg.attach(MIMEText(body, 'plain'))
            server.sendmail(sender_email, email, msg.as_string())
            print(f"Email sent to {email}")
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")
finally:
    server.quit()
