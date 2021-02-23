import redis

from common.urls.urls_file import redis_connection

conn = redis.Redis(
    '{}'.format(redis_connection['host']), redis_connection['port'],
    charset="utf-8", decode_responses=True)
