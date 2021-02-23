from kombu import Connection

from common.urls.urls_file import rabbit_connection

rabbit_url = "{}".format(rabbit_connection)
conn = Connection(rabbit_url)
channel = conn.channel()
