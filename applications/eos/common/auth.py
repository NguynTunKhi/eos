import base64
import os
from applications.eos.enums import auth


def validate_basic_auth_token(auth_header):
    auth_token = auth_header.split(' ')
    if len(auth_token) != 2:
        return False
    else:
        try:
            plain_auth_token = str(base64.b64decode(auth_token[1]))
        except Exception as ex:
            return False
        userpass = plain_auth_token.split(':')
        if len(userpass) != 2:
            return False
        else:
            user = userpass[0]
            password = userpass[1]
            auth_user = os.getenv(auth.ENV_USER_BASIC_AUTH_API)
            auth_pass = os.getenv(auth.ENV_PASSWORD_BASIC_AUTH_API)
            if user != auth_user or password != auth_pass:
                return False
            return True