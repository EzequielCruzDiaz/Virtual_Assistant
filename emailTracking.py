import smtplib
from email.mime.text import MIMEText

subject = "Test message"
body = "i am harmony, i hope you being good today, this is just a test about automatizing emails, IDK if the correct term, but you probably got it"
sender = "ezequielcruz018@gmail.com"
recipients=[""]
password="luwb sxlt rcip vrej"

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