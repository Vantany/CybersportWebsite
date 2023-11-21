import smtplib
from email.mime.text import MIMEText
from data import db_session
from data.participants import Participant
import main


def send_email(subject_id, message):
    sender = "....@gmail.com"
    password = ""

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    participant = main.get_participant(subject_id)
    if participant:
        subject = participant.contact
    else:
        return "Неправильный id пользователя"

    try:
        server.login(sender, password)

        fixed_msg = MIMEText(message)
        fixed_msg["Subject"] = subject

        server.sendmail(sender, sender, fixed_msg.as_string())
        server.sendmail(sender, sender, f"Subject: {subject}\n{message}")

        return "The message was sent successfully!"

    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please"
