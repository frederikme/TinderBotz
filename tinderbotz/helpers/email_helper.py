import smtplib
from email.message import EmailMessage

class EmailHelper:

    # I created a gmail account for everyone to use, please don't abuse this.
    @staticmethod
    def send_mail_match_found(to):
        match_msg = "Congratulations you've been matched with someone. Please check your profile for more details."

        msg = EmailMessage()
        msg.set_content(match_msg)

        msg['Subject'] = 'NEW TINDER MATCH'
        msg['From'] = "github.tinderbotz@gmail.com"
        msg['To'] = to

        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("github.tinderbotz@gmail.com", "kuzdys-1zafri-Pebzob")
        server.send_message(msg)
        server.quit()
