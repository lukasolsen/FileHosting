import uuid
import datetime
from werkzeug.security import generate_password_hash

AUTH_EXPIRATION_TIME = datetime.timedelta(days=7)
DOWNLOAD_LINKS = {}
SECRET_KEY = "secret"


def generate_download_token(file_identifier):
    token = generate_password_hash(
        file_identifier + SECRET_KEY, salt_length=10)
    DOWNLOAD_LINKS[token] = file_identifier
    return token


def is_valid_token(token):
    return token in DOWNLOAD_LINKS


def get_file_identifier(token):
    return DOWNLOAD_LINKS.get(token)


def clean_expired_tokens():
    now = datetime.datetime.utcnow()
    expired_tokens = [token for token, expiration_time in DOWNLOAD_LINKS.items(
    ) if expiration_time < now]
    for token in expired_tokens:
        DOWNLOAD_LINKS.pop(token)
