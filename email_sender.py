import smtplib
from email.mime.text import MIMEText


def send_email(subject, message):
    sender = "....@gmail.com"
    password = ""
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        
        fixed_msg = MIMEText(message)
        fixed_msg["Subject"] = subject 
        
        server.sendmail(sender, sender, fixed_msg.as_string())
        server.sendmail(sender, sender, f"Subject: {subject}\n{message}")  
        
        return "The message was sent successfully!"
    
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please"