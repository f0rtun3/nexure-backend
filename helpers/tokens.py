"""
User account confirmation token handler
generates user token for account confirmation and verifies the same
"""
from flask_jwt_extended import (create_access_token, create_refresh_token)


def user_account_confirmation_token(identity):
    """
    generate a token to confirm user account
    :param identity:
    :return:
    """
    user_confirmation_token = create_access_token(identity=identity)

    return user_confirmation_token


def tokens(access_token, refresh_token):
    """
    return user authentication dictionary
    :param access_token:
    :param refresh_token:
    :return:
    """
    auth_tokens = {'access_token': access_token, 'refresh_token': refresh_token}
    return auth_tokens


def create_user_token(identity):
    """
    the identity of the token contained will be the user id(serial)
    :param identity:
    :return: dictionary
    """
    user_access_token = create_access_token(identity=identity, fresh=True)
    user_refresh_token = create_refresh_token(identity=identity)
    auth_tokens = tokens(user_access_token, user_refresh_token)
    return auth_tokens


def refresh_user_token(identity):
    """
    generate a refresh token once an access token has expired after one hour
    :param identity:
    :return: string
    """
    user_refresh_token = create_access_token(identity=identity, fresh=False)
    return user_refresh_token

