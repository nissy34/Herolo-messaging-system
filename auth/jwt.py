from config import SECRET_KEY
import datetime
import jwt


def encode_auth_token(username):
    """
    Generates the Auth Token
    :return: string
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )



def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: string
    """
    # try:
    payload = jwt.decode(auth_token, SECRET_KEY)
    return payload['sub']
    # except jwt.ExpiredSignatureError:
    #     return 'Signature expired. Please log in again.'
    # except jwt.InvalidTokenError:
    #     return 'Invalid token. Please log in again.'