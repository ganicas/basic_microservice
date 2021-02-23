import os
import json

# Database setup
databases = json.loads(os.environ['DATABASE_CONNECTION'])
robot_database_connection = databases['robot_database']
master_app_database_connection = databases['master_app_database']

# Rabbit mq connection
rabbit_connection = os.environ['RABBIT_MQ']

# Redis connection
redis_connection = json.loads(os.environ['REDIS_URI'])