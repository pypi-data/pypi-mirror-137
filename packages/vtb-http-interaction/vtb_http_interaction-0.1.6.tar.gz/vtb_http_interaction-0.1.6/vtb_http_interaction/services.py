# pylint: disable=too-few-public-methods
import asyncio
import logging
import warnings
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Tuple, Dict, Optional, Union, FrozenSet
from vtb_py_logging.request_id import get_context_request_id
from aiohttp import ClientSession, ContentTypeError
from aiohttp.web_exceptions import HTTPUnauthorized
from jose import exceptions
from vtb_http_interaction import http_utils

from vtb_http_interaction.errors import MaxRetryError, RetryError
from vtb_http_interaction.keycloak_gateway import KeycloakConfig
from vtb_http_interaction.process_authorization_header import ProcessAuthorizationHeader


class OnErrorResult(Enum):
    """
    SILENT - проигнорировать ошибку
    THROW - возбудить ошибку
    REFRESH - при ошибке выполнить действие повторно
    """
    SILENT = 1
    THROW = 2
    REFRESH = 3


class BaseService(ABC):
    """
    Abstract service
    """

    # TODO: max_retry, retry_on_statuses, backoff_factor - атрибуты датакласса, который является параметром конструктора
    def __init__(self, max_retry: Optional[int] = 5,
                 retry_on_statuses: Optional[FrozenSet[Union[int, str]]] = frozenset({413, 429, 503, 504}),
                 backoff_factor: Optional[int] = 0.2):
        """
        Сервис
        :param max_retry: максимальное количество повторений
        :param retry_on_statuses: коды HTTP, после которых требуется произвести повтор запроса
        :param backoff_factor: коэффициент задержки попыток повторных вызовов
        """
        self.logger = logging.getLogger(__name__)
        self.current_step = 0
        self.max_retry = max_retry
        self.backoff_factor = backoff_factor
        self.retry_on_statuses = frozenset({int(status) for status in retry_on_statuses} if retry_on_statuses else {})

    @abstractmethod
    async def _send(self, *args, **kwargs) -> Any:
        """
        Abstract _send
        """
        raise NotImplementedError("Not implemented _send method")

    async def send_request(self, *args, **kwargs) -> Any:
        """
        Вызов внешнего сервиса
        """

        try:
            args, kwargs = await self._before_send(*args, **kwargs)
            self.logger.debug("Send request %s: %s; %s", self.current_step, args, kwargs)
            response = await self._send(*args, **kwargs)
            self.logger.debug("Response %s: %s", self.current_step, response)

            if self.retry_on_statuses and response[0] in self.retry_on_statuses:
                raise RetryError()

            # обнуляем current_step для запроса, он выполнен успешно
            self.current_step = 0
            return response
        except Exception as ex:
            need_retry = isinstance(ex, RetryError)
            # TODO: self._on_error не должно ничего возвращать. Замена:
            # OnErrorResult.SILENT - загасить ошибку можно явно в _on_error
            # OnErrorResult.THROW - выполнить raise в самом конце блока
            # OnErrorResult.REFRESH - вызвать исключение RetryError для повтора

            on_error_result = OnErrorResult.REFRESH if need_retry else await self._on_error(ex, *args, **kwargs)

            if on_error_result == OnErrorResult.THROW:
                self._raise_exception(ex)
            if on_error_result == OnErrorResult.SILENT:
                self.logger.exception(ex)
                return None
            if on_error_result == OnErrorResult.REFRESH:
                return await self._resend_request(ex, *args, **kwargs)

            raise NotImplementedError(f"on_error_result \"{on_error_result}\" not implemented") from ex

    def _raise_exception(self, ex: Exception) -> None:
        self.logger.exception(ex)
        raise ex

    async def _before_send(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """
        Действие перед вызовом
        """
        return args, kwargs

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:  # pylint: disable=unused-argument
        """
        Действие на возникновение ошибки.
        SILENT - продолжить работу без возникновения ошибки
        THROW - выкинуть исключение дальше
        REFRESH - сделать повторный вызов сервиса
        """
        return OnErrorResult.THROW

    async def _resend_request(self, ex: Exception, *args, **kwargs) -> Any:
        """ Повторная отправка запроса """
        self.current_step += 1

        self.logger.debug('Repeat request #%s.', self.current_step)

        if self.current_step >= self.max_retry:
            raise MaxRetryError(f'Exceeded the maximum number of attempts {self.max_retry}') from ex

        sleep_seconds = self.backoff_factor * (2 ** (self.current_step - 1))
        await asyncio.sleep(sleep_seconds)

        return await self.send_request(*args, **kwargs)


class HttpService(BaseService):
    """
    Вызов по протоколу http
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _send(self, *args, **kwargs) -> Any:
        method = kwargs.get('method', 'get')

        url = kwargs.get('url', None)
        if url is None:
            raise ValueError("Url is none")
        url = str(url)

        cfg = kwargs.get('cfg', {})
        assert isinstance(cfg, dict)

        if url.lower().startswith('https://') and 'ssl' not in cfg:
            cfg['ssl'] = False

        async with ClientSession(json_serialize=http_utils.dumps) as session:
            async with session.request(method, url, **cfg) as response:
                status = response.status
                if status == 401:
                    response_content = response.text()
                    self.logger.debug("Unauthorized response %s: %s", self.current_step, response_content)
                    raise HTTPUnauthorized()

                # ContentTypeError
                try:
                    response_data = await response.json()
                except ContentTypeError:
                    response_data = await response.text()
                # TODO: Могут потребоваться не только статус и ответ, а еще что-то, например, заголовки,
                #  возможно сделать датакласс
                return status, response_data


class RestService(HttpService):
    """
    Вызов rest сервисов
    """

    def __init__(self, url: str, item_url_postfix: Optional[str] = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if url is None:
            raise ValueError("url is none.")

        self.url = url
        self.item_url_postfix = item_url_postfix

    async def post(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP POST request.
        """
        kwargs['method'] = "POST"
        kwargs['url'] = self.url

        return await self.send_request(*args, **kwargs)

    async def get(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP GET request.
        """

        kwargs['method'] = "GET"
        kwargs['url'] = self._prepare_item_url(kwargs['item_id']) if 'item_id' in kwargs else self.url

        return await self.send_request(*args, **kwargs)

    async def put(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP PUT request.
        """

        kwargs['method'] = "PUT"
        kwargs['url'] = self._prepare_item_url(kwargs.get('item_id', None))

        return await self.send_request(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP DELETE request.
        """

        kwargs['method'] = "DELETE"
        kwargs['url'] = self._prepare_item_url(kwargs.get('item_id', None))

        return await self.send_request(*args, **kwargs)

    def _prepare_item_url(self, item_id: str) -> str:
        if item_id is None:
            raise ValueError('Request must contain an id.')

        item_id = str(item_id)

        if item_id.startswith('/'):
            item_id = item_id[1:]

        url = self.url
        if url.endswith('/'):
            url = url[:-1]

        return f"{url}/{item_id}{self.item_url_postfix}"


# TODO: Вынести миксины в отдельный файл mixins.py в версии 1.0.0
# TODO: Отказаться от миксинов, вместо них можно использовать декомпозицию. В конструктор базового сервиса передавать
#  список объектов, которые будут обогащать хидеры (на подобие django middleware).
#  middleware, отвечающий за заголовок авторизации не должен знать где ему кешировать заголовок.
#  Он также должен принимать в конструкторе объект кеша.
# noinspection PyClassHasNoInit
class PrepareHeaderMixin:
    """ Миксин подготовки хидеров """

    async def prepare_header(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """ Подготовка хидеров """
        return args, kwargs

    async def _before_send(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """ Переопределяем _before_send у класса, к которому применен миксин """
        return await self.prepare_header(*args, **kwargs)


# noinspection PyClassHasNoInit
class RequestIdHeaderMixin(PrepareHeaderMixin):
    """ добавление заголовка X-Request-Id к запросу """

    async def prepare_header(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """ Подготовка хидеров """
        request_id = get_context_request_id()
        if request_id:
            headers = kwargs.setdefault("cfg", {}).setdefault("headers", {})
            headers["X-Request-Id"] = request_id
        args, kwargs = await super().prepare_header(*args, **kwargs)
        return args, kwargs


# noinspection PyClassHasNoInit
class AuthorizationPrepareHeaderMixin(PrepareHeaderMixin):
    """Обработка заголовка Authorization"""
    process_authorization_header = None

    async def prepare_header(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """ Действие перед вызовом """
        args, kwargs = await super().prepare_header(*args, **kwargs)
        kwargs = await self.process_authorization_header.prepare_header(**kwargs)

        return args, kwargs

    async def obtain_token(self, ex: Exception, **kwargs) -> OnErrorResult:
        """
        Действие на возникновение ошибки ExpiredSignatureError, HTTPUnauthorized
        В случае обновления токена возвращаем OnErrorResult.REFRESH для повторного вызова сервиса с новым заголовком
        На все остальные ошибки вернуть OnErrorResult.THROW
        """
        # Повторные вызовы (а значит и обновление access_token) запрещены, либо нет refresh_token (нечем обновлять)
        if not self.max_retry or not self.process_authorization_header.refresh_token:
            self._raise_exception(HTTPUnauthorized())

        if isinstance(ex, HTTPUnauthorized):
            # Пара токенов закеширована, но по каким-то причинам они стали недействительны,
            # нужно очистить кеш и запросить новые токены
            await self.process_authorization_header.clear_cache()
            return OnErrorResult.REFRESH

        if isinstance(ex, exceptions.ExpiredSignatureError):
            # access_token просрочен
            # Есть refresh_token и можно попытаться обновить access_token
            await self.process_authorization_header.obtain_token(**kwargs)
            return OnErrorResult.REFRESH

        return OnErrorResult.THROW


class HttpServiceWithRequestId(RequestIdHeaderMixin, HttpService):
    """ HttpService с заголовком X-Request-Id """


class RestServiceWithRequestId(RequestIdHeaderMixin, RestService):
    """ RestService с заголовком X-Request-Id """


# TODO: Убрать сервисы Authorization**, из заменят HttpService и RestService с обработчиками заголовков в конструкторе
# TODO: Сделать утилитарную функцию, для создания таких сервисов

# Группа сервисов, реализующих логику получения токена из keycloak и сохранения его в редис
class AuthorizationHttpService(RequestIdHeaderMixin, AuthorizationPrepareHeaderMixin, HttpService):
    """ Вызов http сервисов под УЗ пользователя Keycloak """

    def __init__(self,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: Optional[str] = None,
                 token_cache=None,
                 max_retry: Optional[int] = 5):
        super().__init__(max_retry=max_retry)
        # TODO: Убрать redis_connection_string в версии 1.0.0, его заменяет token_cache
        warnings.warn(
            "init parameter 'redis_connection_string' is deprecated, use 'token_cache' instead. "
            "The class will be removed in version 1.0.0.",
            DeprecationWarning, stacklevel=2
        )
        self.process_authorization_header = ProcessAuthorizationHeader(keycloak_config,
                                                                       redis_connection_string=redis_connection_string,
                                                                       token_cache=token_cache)

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:
        return await self.obtain_token(ex, **kwargs)


# pylint: disable=too-many-ancestors,too-many-arguments
class AuthorizationService(RequestIdHeaderMixin, AuthorizationPrepareHeaderMixin, RestService):
    """ Вызов rest сервисов под УЗ пользователя Keycloak """

    def __init__(self,
                 url: str,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: Optional[str] = None,
                 token_cache=None,
                 item_url_postfix: Optional[str] = '',
                 max_retry: Optional[int] = 5):
        # TODO: Удалить класс в версии 1.0.0
        warnings.warn(
            "class AuthorizationService is deprecated, use AuthorizationRestService instead. "
            "The class will be removed in version 1.0.0.",
            DeprecationWarning, stacklevel=2
        )
        super().__init__(url, item_url_postfix, max_retry=max_retry)
        self.process_authorization_header = ProcessAuthorizationHeader(keycloak_config,
                                                                       redis_connection_string=redis_connection_string,
                                                                       token_cache=token_cache)

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:
        return await self.obtain_token(ex, **kwargs)


AuthorizationRestService = AuthorizationService
