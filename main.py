import smtplib
import ssl
import imaplib
import email
import os

try:
    password = os.environ["EMAIL_PASSWORD"]
except KeyError:
    password = "Token not available!"

agent_email = "kallax.brueder.wg@gmail.com"

def send_mail(receiver=agent_email, subject=" ", message=" "):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(agent_email, password)

        server.sendmail(agent_email, receiver, f'Subject: {subject} \n\n{message}')
        server.quit()


def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()


def receive_latest_email():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(agent_email, password)
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox")  # connect to inbox.

    result, data = mail.uid('search', None, "ALL")  # search and return uids instead
    latest_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    print(msg['Subject'])
    print(get_first_text_block(msg))

if __name__ == "__main__":
    send_mail(agent_email, "github tets", "This is an email test from github actions")
#receive_latest_email()
