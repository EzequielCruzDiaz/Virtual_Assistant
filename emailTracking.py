import smtplib
from email.mime.text import MIMEText

subject = "Test message"
body = "your message here"
sender = "your email here "
recipients=["Destiny email here"]
password="your gmail api password here"

def send_email(subject,body,sender,recipients,password):
    msg = MIMEText(body)
    msg['subject'] = subject
    msg['From'] = sender
    msg['To'] = ''.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender,password)
        smtp_server.sendmail(sender,recipients,msg.as_string())
    print("Message sent!")

send_email(subject, body, sender,recipients,password)