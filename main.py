import smtplib
import ssl
import imaplib
import email
import os
import csv

try:
    password = os.environ["EMAIL_PASSWORD"]
except KeyError:
    password = "Token not available!"

agent_email = "kallax.brueder.wg@gmail.com"


class Agent:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def daily_check(self):
        # TODO: Implement check that runs every day to decide what to do
        pass

    def assign_people_to_cleaning_area(self):
        # TODO: Implement assignment
        pass

    def send_mail(self, receiver=agent_email, subject=" ", message=" "):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(agent_email, password)

            server.sendmail(agent_email, receiver, f'Subject: {subject} \n\n{message}')
            server.quit()

    def get_first_text_block(self, email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()

    def receive_latest_email(self):
        # TODO: Change this to check if user has sent mail this past week (confirmation of cleaning)
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
        print(self.get_first_text_block(msg))

    def read_points_from_file(self, user=None):
        data = []
        with open("penalty_points.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        # Returns the points as an int for a SPECIFIED user
        if user:
            user_data = next((row for row in data if row["User"] == user), None)
            return user_data

        # Returns the general data for ALL users
        else:
            return data

    def write_points_to_file(self, user, action):
        data = self.read_points_from_file()

        user_data = next((row for row in data if row["User"] == user), None)
        user_points = int(user_data["Penalties"])

        if action == "add":
            user_points += 1

        elif action == "subtract":
            user_points -= 1

        user_data["Penalties"] = str(user_points)

        with open("penalty_points.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def read_scheduled_dates_from_file(self):
        # TODO: Implement
        pass

    def write_scheduled_dates_to_file(self, scheduled_dates):
        # TODO: Implement
        pass

if __name__ == "__main__":
    agent = Agent(agent_email, password)
    agent.daily_check()
