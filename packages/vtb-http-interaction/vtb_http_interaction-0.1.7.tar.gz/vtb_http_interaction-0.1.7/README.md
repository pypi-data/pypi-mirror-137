# Межсервисное взаимодействие на основе протокола HTTP

## Описание

Утилитарный пакет, содержащий в себе интеграционный модуль с Keycloak и инструменты для организации межсервисного
взаимодействия на основе протокола HTTP.

## Предусловие

Сервис, который выступает источником данных должен быть зарегистрирован в Kong.  
Сервис, который выступает в роли инициатора запроса должен иметь системуную УЗ, которая регистрируется в Keycloak.  
[Подробности](http://wiki.corp.dev.vtb/pages/viewpage.action?pageId=204909264)

## Установка библиотеки

```
pip install vtb_http_interaction
```

с инструментами тестирования и проверки качества кода

```
pip install vtb_http_interaction[test]
```

## Тестирование

Запуск процесса тестирования

```
pytest
```

Внимание! Тесты test_access_token_lifespan и test_access_token_lifespan_with_portal_token выполняют проверку процесса
обновления токена после его устаревания. Время выполнения > 2 мин. Для исключения "долгих" тестов используй команду

```
pytest -m "not slow"
```

## Быстрый старт

### Интеграционный модуль с Keycloak

Создание объекта KeycloakConfig на основе переменных окружения

```python
from vtb_http_interaction.http_utils import make_environ_keycloak_config

keycloak_config = make_environ_keycloak_config()
print(keycloak_config)
# KeycloakConfig(server_url='server_url', realm_name='realm_name', client_id='client_id', client_secret_key='client_secret_key', verify=False, custom_headers=None)
```

Получение токена сервисной УЗ

```python
from dotenv import load_dotenv
from envparse import env

from vtb_http_interaction.keycloak_gateway import KeycloakGateway, KeycloakConfig

load_dotenv()

keycloak_config = KeycloakConfig(
    server_url=env.str('KEYCLOAK_SERVER_URL'),
    client_id=env.str('KEYCLOAK_CLIENT_ID'),
    realm_name=env.str('KEYCLOAK_REALM_NAME'),
    client_secret_key=env.str('KEYCLOAK_CLIENT_SECRET_KEY')
)

with KeycloakGateway(keycloak_config) as gateway:
    token = gateway.obtain_token()
```

Получение токена пользователя из кейклок

```python
from dotenv import load_dotenv
from envparse import env

from vtb_http_interaction.keycloak_gateway import KeycloakGateway, KeycloakConfig, UserCredentials

load_dotenv()

keycloak_config = KeycloakConfig(
    server_url=env.str('KEYCLOAK_SERVER_URL'),
    client_id=env.str('KEYCLOAK_CLIENT_ID'),
    realm_name=env.str('KEYCLOAK_REALM_NAME'),
    client_secret_key=env.str('KEYCLOAK_CLIENT_SECRET_KEY')
)

user_credentials = UserCredentials(
    username=env.str('KEYCLOAK_TEST_USER_NAME'),
    password=env.str('KEYCLOAK_TEST_USER_PASSWORD')
)

with KeycloakGateway(keycloak_config) as gateway:
    token = gateway.obtain_token(user_credentials,
                                 grant_type=("password",))
```

### Пример реализации межсервисного взаимодействия через Kong

```python
from dotenv import load_dotenv
from envparse import env

from vtb_http_interaction.keycloak_gateway import KeycloakConfig

from vtb_http_interaction.services import AuthorizationRestService

load_dotenv()

authorizer_ser_list_url = env.str('AUTHORIZER_USER_LIST_URL')
redis_url = env.str('REDIS_URL')

keycloak_config = KeycloakConfig(
    server_url=env.str('KEYCLOAK_SERVER_URL'),
    client_id=env.str('KEYCLOAK_CLIENT_ID'),
    realm_name=env.str('KEYCLOAK_REALM_NAME'),
    client_secret_key=env.str('KEYCLOAK_CLIENT_SECRET_KEY')
)

service = AuthorizationRestService(authorizer_ser_list_url,
                                   keycloak_config,
                                   redis_url)
params = {
    "page": 1,
    "per_page": 20
}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

status, response = await service.get(cfg={'params': params, 'headers': headers})

```

### Инструменты для организации межсервисного взаимодействия на основе протокола HTTP

Вызов удаленного HTTP метода

```python
from vtb_http_interaction.services import HttpService

service = HttpService()

status, response = await service.send_request(
    method="GET",
    url="http://example.com/api/v1/comments?boardId=6b681e1558384da3a5d4b22a33417181")
```

Вызов удаленного REST API метода для списка комментариев с использованием фильра по boardId

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

status, response = await service.get(cfg={'params': {"boardId": "6b681e1558384da3a5d4b22a33417181"}})
```

Вызов удаленного REST API метода для получения комментария с ID=1

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

status, response = await service.get(item_id=1)
```

Вызов удаленного REST API метода для создания комментария

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

data = {
    "content": "Привет медвед!",
    "boardId": "6b681e1558384da3a5d4b22a33417181",
    "userName": "User 1"
}

status, response = await service.post(cfg={'json': data})
```

Вызов удаленного REST API метода для обновления комментария с ID=1

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

update_data = {
    "content": "Привет медвед new!",
}

status, response = await service.put(item_id=1, cfg={'json': update_data})
```

Вызов удаленного REST API метода для удаления комментария с ID=1

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

status, response = await service.delete(item_id=1)
```

### HTTP Utils

Парсинг значения заголовка Authorization

```python
from vtb_http_interaction.http_utils import parse_authorization_header

key, token = parse_authorization_header('bearer 401f7ac837da42b97f613d789819ff93537bee6a')
assert key == 'bearer'
assert token == '401f7ac837da42b97f613d789819ff93537bee6a'
```

# Реализация классов, отвечающих за кеширование access_token и refresh_token

Для выбора того, какой механизм кеширования access_token и refresh_token использовать, конструктор сервисов
AuthorizationHttpService и AuthorizationRestService имеет параметр token_cache. Это экземпляр класса, который реализует
следующий протокол:

1. необходимые методы класса: set_value, get_value
2. необязательные методы класса: init, dispose

Если определен token_cache, то используется указанный объект, если redis_connection_string, то RedisCache, в противном
случае выдается исключение ValueError. Т.о. один из параметров token_cache или redis_connection_string обязателен.  
Доступные реализации классов, отвечающие за кеширование:

1. MemoryCache - кеширование токенов в памяти
2. RedisCache - кеширование токенов в redis

Пример создания сервиса AuthorizationRestService с использованием MemoryCache

```python
from vtb_http_interaction.process_authorization_header import MemoryCache

service = AuthorizationRestService(authorizer_user_list_url,
                                   keycloak_config,
                                   token_cache=MemoryCache())
```

Пример создания сервиса AuthorizationRestService с использованием RedisCache

```python
from vtb_http_interaction.process_authorization_header import RedisCache

service = AuthorizationRestService(authorizer_user_list_url,
                                   keycloak_config,
                                   token_cache=RedisCache(redis_url))
```