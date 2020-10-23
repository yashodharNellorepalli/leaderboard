from .utils.helpers import get_redis_connection, get_request


def decorator_redis_connection(callback):
    def wrapper(*args, **kwargs):
        request = get_request(args)
        redis_connection = get_redis_connection()

        request.redis_connection = redis_connection

        return callback(*args, **kwargs)

    return wrapper
