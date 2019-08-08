from app import app, mail
from flask_mail import Message


class Email(object):
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self._text = None
        self._html = None

    def text(self, text):
        self._text = text

    def html(self, html):
        self._html = html

    def send(self, from_addr):
        self.to = [self.to]
        if not self.text and self.html:
            raise Exception('Email must contain a body')
        msg = Message(
            self.subject,
            sender=from_addr,
            recipients=self.to
        )
        if self.text:
            msg.body = self.text
        if self.html:
            msg.html = self.html

        mail.send(msg)
