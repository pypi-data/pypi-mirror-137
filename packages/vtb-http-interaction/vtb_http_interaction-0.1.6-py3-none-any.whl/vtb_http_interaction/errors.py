class RetryError(Exception):
    """
    Ошибка, которая вызывает повторный вызов запроса
    """


class MaxRetryError(Exception):
    """
    Превышено максимальное число повторов
    """


class InvalidToken(Exception):
    """
    Заголовок Authorization не соответствует формату
    Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """
