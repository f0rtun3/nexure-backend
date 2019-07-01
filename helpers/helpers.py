from flask import jsonify, render_template
from flask_mail import Message
from app import app, mail
import hashlib


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


def send_email(recipient, subject, template):
    msg = Message(
        subject,
        recipients=[recipient],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


"""
def generate_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def confirm_user_password(db_pwd, user_pwd):
    user_pwd_hash = generate_hash(user_pwd)

    return user_pwd_hash == db_pwd
"""
