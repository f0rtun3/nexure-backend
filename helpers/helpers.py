from flask import jsonify, render_template
from botocore.exceptions import ClientError
from app import app, ses
import string
import random
# from helpers import Mailer


def make_rest_fail_response(message):
    return jsonify({"status_message": "failed", "message": message})


def make_rest_success_response(message=None, payload=None):
    if payload is None:
        payload = {}

    return jsonify({"status_message": "success", "message": message, "payload": payload})


def generate_confirmation_template(url_endpoint, code):
    html = render_template('activate.html',
                           url_endpoint=url_endpoint,
                           confirm_token=code)
    return html


def generate_temporary_password_template(url_endpoint, code):
    html = render_template('temp_password.html',
                           url_endpoint=url_endpoint,
                           temp_password=code)
    return html


def send_email(recipient, subject, template, email_text):
    sender=app.config['MAIL_DEFAULT_USER']
    recipient = [recipient]
    try:
        response = ses.send_email(
            Source=sender,
            Destination={
                'ToAddresses': recipient
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': email_text
                    },
                    "Html": {
                        'Data': template
                    }
                }
            }
        )
    except ClientError as e:
        return f"{e.response['Error']['Message']}"
    else:
        return "success"
    """
    if not from_addr:
        from_addr = app.config['MAIL_DEFAULT_USER']
    email = Mailer.Email(recipient, subject)
    email.html(template)
    email.send(from_addr)
    """


def create_user_password():
    """
    generate a random password for user
    :return: password   string
    """
    string_length = 7
    password = string.ascii_letters + string.digits

    return ''.join(random.choice(password) for i in range(string_length))


def get_customer_id(customer_number):
    """ get the customer id from the customer number with format (type/year/customer_id/country)
   :param customer_number  string 
   :return customer_id     int
   """
    customer_number_array = customer_number.split('/')
    customer_id = int(customer_number_array[2])

    return customer_id


def get_customer_type(customer_number):
    """ we might need to know whether the customer type is an individual or organization
    :param customer_number:
    :return:
    """
    cust_number_array = customer_number.split('/')
    cust_type = cust_number_array[0]

    return cust_type
