"""
Реализация классов, отвечающих за алгоритмы получения и сохранения токенов аутентификации
"""
import time
from typing import Tuple, Any, Dict, Union, Optional

import aioredis

from vtb_http_interaction.http_utils import parse_authorization_header
from vtb_http_interaction.keycloak_gateway import KeycloakGateway, KeycloakConfig


# TODO: Вынести классы *Cache в отдельный файл cache.py либо в отдельный пакет в версии 1.0.0
# TODO: Сделать в set_value так, чтобы она принимала не access_token: str, refresh_token: str, а cache_value: Any

class MemoryCache:
    """
    Класс, реализующий хранение access_token и refresh_token в памяти
    """
    memory_cache = {}
    _time_dict = {}

    def __init__(self, expired_timeout: Optional[float] = 300):
        """
        expired_timeout - время устаревания кэша по умолчанию, в секундах.
        По умолчанию 300 секунд (5 минут). Вы можете установить expired_timeout в None, тогда кэш никогда не устареет.
        Если указать 0, все ключи будут сразу устаревать (таким образом можно заставить «не кэшировать»).
        """
        self.expired_timeout = expired_timeout

    async def set_value(self, cache_key: str, access_token: str, refresh_token: str) -> None:
        """ Установка значения токена """
        cache_value = {'access_token': access_token, 'refresh_token': refresh_token}

        self.memory_cache[cache_key] = cache_value
        self._set_expiration_time(cache_key)

    async def get_value(self, cache_key: str) -> Tuple[Union[None, str], Union[None, str]]:
        """ Получение значения токена """
        if not self._key_is_expired(cache_key):
            result = self.memory_cache.get(cache_key, {})
            return result.get('access_token', None), result.get('refresh_token', None)

        return None, None

    async def delete_key(self, cache_key: str):
        """ Очистка кеша по ключу """
        if cache_key in self.memory_cache:
            self.memory_cache.pop(cache_key)

    def _key_is_expired(self, cache_key: str) -> bool:
        """ Проверка срока жизни ключа """
        if self.expired_timeout is None:
            return False

        if self.expired_timeout == 0:
            return True

        if cache_key in self._time_dict:
            return time.time() > self._time_dict[cache_key]

        return True

    def _set_expiration_time(self, cache_key: str):
        """ Установка времени устаревания ключа """
        self._time_dict[cache_key] = time.time() + self.expired_timeout


class RedisCache:
    """
    Класс, реализующий хранение access_token и refresh_token в redis
    Необходимая реализация протокола: set_value, get_value
    Необязательная реализация протокола: init, dispose
    """

    def __init__(self, redis_connection_string: str, close_connection: Optional[bool] = True):
        self.redis_connection_string = redis_connection_string
        self.redis_pool = None
        self.close_connection = close_connection

    async def set_value(self, cache_key: str, access_token: str, refresh_token: str) -> None:
        """ Установка значения токена """
        cache_value = {'access_token': access_token, 'refresh_token': refresh_token}
        await self.delete_key(cache_key)

        await self.redis_pool.hset(cache_key, mapping=cache_value)

    async def get_value(self, cache_key: str) -> Tuple[Union[None, str], Union[None, str]]:
        """ Получение значения токена """
        key_exist = await self.redis_pool.exists(cache_key)
        if key_exist:
            result = await self.redis_pool.hgetall(cache_key)
            return result.get('access_token', None), result.get('refresh_token', None)

        return None, None

    async def delete_key(self, cache_key: str):
        """ Очистка кеша по ключу """
        key_exist = await self.redis_pool.exists(cache_key)
        if key_exist:
            await self.redis_pool.delete(cache_key)

    async def init(self):
        """ Инициализация ресурсов """
        self.redis_pool = aioredis.from_url(self.redis_connection_string, decode_responses=True)

    async def dispose(self):
        """ Освобождение ресурсов """
        if self.close_connection:
            await self.redis_pool.close()


class ProcessAuthorizationHeader:
    """
    Обработка заголовка Authorization
    """

    def __init__(self,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: Optional[str] = None,
                 token_cache=None):
        self.refresh_token = None
        self.keycloak_config = keycloak_config
        self.cache_key = f"{keycloak_config.realm_name}_{keycloak_config.client_id}"
        if token_cache:
            self.token_cache = token_cache
        elif redis_connection_string:
            self.token_cache = RedisCache(redis_connection_string)
        else:
            # TODO: Должна быть возможность работать без кеширования
            raise ValueError('One of the parameters is required: redis_connection_string, token_cache.')

    async def clear_cache(self):
        """ Очистка кеша """
        await self.token_cache.delete_key(self.cache_key)

    async def prepare_header(self, **kwargs) -> Dict[Any, Any]:
        """
        Обработка заголовка Authorization перед вызовом session.request
        Алгоритм:
        0. Получение токена выполнять только, если его нет в заголовке. Если токен есть, то проверяем его срок жизни.
        1. Получаем refresh_token и access_token из Redis. Если токен есть, то проверяем его срок жизни.
        2. Если их нет, то запрашиваем их на основе логина/пароля. Кладем их в Redis
        3. Формируем заголовок к запросу 'Authorization': "Bearer {access_token}"
        :param kwargs: параметры запроса
        :return: обработанные параметры запроса
        """
        if not _authorization_header_exist(**kwargs):
            await self._init()

            try:
                access_token, self.refresh_token = await self.token_cache.get_value(self.cache_key)

                if self.refresh_token is None or access_token is None:
                    with KeycloakGateway(self.keycloak_config) as gateway:
                        access_token, self.refresh_token = gateway.obtain_token()

                    await self.token_cache.set_value(self.cache_key, access_token, self.refresh_token)
                else:
                    await self._validate_token_lifespan(access_token)
            finally:
                await self._dispose()

            if 'cfg' not in kwargs:
                kwargs['cfg'] = {}

            if 'headers' not in kwargs['cfg']:
                kwargs['cfg']['headers'] = {}

            if 'Authorization' not in kwargs['cfg']['headers']:
                kwargs['cfg']['headers']['Authorization'] = f'Bearer {access_token}'
        else:
            access_token = _parse_authorization_header(kwargs['cfg']['headers']['Authorization'])
            await self._validate_token_lifespan(access_token)

        return kwargs

    async def obtain_token(self, **kwargs) -> Dict[Any, Any]:
        """
        Обновление access_token
        Алгоритм:
        1. Обновляем access_token на основе refresh_token
        2. Кладем новые access_token и refresh_token в Redis
        :param kwargs: параметры запроса
        :return: обработанные параметры запроса
        """
        if self.refresh_token is None:
            raise ValueError('refresh_token is none')

        with KeycloakGateway(self.keycloak_config) as gateway:
            access_token, self.refresh_token = gateway.obtain_new_token(self.refresh_token)

        await self._init()
        try:
            await self.token_cache.set_value(self.cache_key, access_token, self.refresh_token)

            if _authorization_header_exist(**kwargs):
                del kwargs['cfg']['headers']['Authorization']
        finally:
            await self._dispose()

        return kwargs

    async def _validate_token_lifespan(self, access_token: str) -> bool:
        with KeycloakGateway(self.keycloak_config) as gateway:
            gateway.decode_token(token=access_token, key=gateway.public_key)

        return True

    async def _init(self):
        try:
            await self.token_cache.init()
        except AttributeError:
            pass

    async def _dispose(self):
        try:
            await self.token_cache.dispose()
        except AttributeError:
            pass


def _parse_authorization_header(authorization_header: str) -> str:
    key, token = parse_authorization_header(authorization_header)

    if key.lower() != 'bearer':
        raise Exception(f'Invalid token header "{authorization_header}".')

    return token


def _authorization_header_exist(**kwargs):
    """ Проверка наличия заголовка Authorization в запросе """
    if 'cfg' not in kwargs or 'headers' not in kwargs['cfg']:
        return False

    authorization = kwargs['cfg']['headers'].get('Authorization', None)

    return authorization is not None and str(authorization).lower().startswith('bearer')
