from flask import jsonify, render_template
from flask_mail import Message
from app import app, mail
import string
import random


def make_rest_fail_response(message):
    return jsonify({"status": "failed", "message": message})


def make_rest_success_response(message=None, payload=None):
    if payload is None:
        payload = {}

    return jsonify({"message": message, "payload": payload})


def generate_confirmation_template(url_endpoint, code):
    html = render_template('activate.html',
                           url_endpoint=url_endpoint,
                           confirm_code=code)
    return html


def generate_temporary_password_template(url_endpoint, code):
    html = render_template('temp_password.html',
                           url_endpoint=url_endpoint,
                           temp_password=code)
    return html


def send_email(recipient, subject, template):
    msg = Message(
        subject,
        recipients=[recipient],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def create_user_password():
    string_length = 7
    password = string.ascii_letters + string.digits
    return ''.join(random.choice(password) for i in range(string_length))
