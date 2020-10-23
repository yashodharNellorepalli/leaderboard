import redis
from rest_framework.request import Request


def get_redis_connection():
    return redis.Redis(host='127.0.0.1', port=6379, db=0)


def get_request(args):
    for argument in args:
        if isinstance(argument, Request):
            return argument

    return None
