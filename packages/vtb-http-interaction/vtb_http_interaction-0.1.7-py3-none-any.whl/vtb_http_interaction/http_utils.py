"""
Утилитарный класс работы с HTTP
"""
import datetime
import decimal
import json
import os
import uuid
from typing import Tuple

from vtb_http_interaction import errors
from vtb_http_interaction.keycloak_gateway import KeycloakConfig


def parse_authorization_header(authorization_header: str) -> Tuple[str, str]:
    """
    Парсинг значения заголовка Authorization
    Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """
    auth = authorization_header.split()

    len_auth = len(auth)

    if len_auth == 0:
        raise errors.InvalidToken('Invalid token header. No token provided.')

    if len_auth == 1:
        raise errors.InvalidToken('Invalid token header. No credentials provided.')

    if len_auth > 2:
        raise errors.InvalidToken('Invalid token header. Token string should not contain spaces.')

    return auth[0], auth[1]


def default_encoder(obj):
    """ Default JSON encoder """
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

    if isinstance(obj, (uuid.UUID, decimal.Decimal)):
        return str(obj)

    return obj


def dumps(*args, **kwargs):
    """ Сериализация в json """
    return json.dumps(*args, **kwargs, default=default_encoder)


def make_environ_keycloak_config() -> KeycloakConfig:
    """ Создание объекта KeycloakConfig на основе переменных окружения """
    keycloak_config = KeycloakConfig(
        server_url=os.environ.get('KEYCLOAK_SERVER_URL', None) or os.environ.get('KEY_CLOAK_SERVER_URL', None),
        client_id=os.environ.get('KEYCLOAK_CLIENT_ID', None) or os.environ.get('KEY_CLOAK_CLIENT_ID', None),
        realm_name=os.environ.get('KEYCLOAK_REALM_NAME', None) or os.environ.get('KEY_CLOAK_REALM_NAME', None),
        client_secret_key=os.environ.get('KEYCLOAK_CLIENT_SECRET_KEY', None) or os.environ.get(
            'KEY_CLOAK_CLIENT_SECRET_KEY', None)
    )
    return keycloak_config
