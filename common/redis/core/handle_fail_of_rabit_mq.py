from common.logging.setup import logger
from common.redis.connection.connection import conn
from common.robot_data_handler.robot_data_procesing.data_validator.validation_const import RobotDataParser

logger_api = logger


class RedisHandler(object):
    """
    RedisHandler for exception if RabbitMQ fail on sending or receiving messages.
    It will store temporarily data and if RabbitMQ is up and running it will provide all
    processes  to RabbitMQ.
    """
    @classmethod
    def set_redis_validation_fail_process(cls, process_data, process_type, robot_id, company_id):
        """
        :param process_data: JSON object of import
        :param process_type: process type for specific JSON hash
        :param robot_id:
        :param company_id:
        :return: it will only store data with no response
        """
        conn.hmset("{}_{}_{}".format(process_type, robot_id, company_id), process_data)
        logger_api.info("RabbitMQ fail storing data to Redis: {}" % process_data)

    @classmethod
    def return_all_data_from_redis_by_key(cls, process_type):
        """

        :param process_type:
        :return: it will return all data from redis in one call
        """
        append_keys = []

        for key in conn.scan_iter():
            split = str(key).split('_')
            key_split = split[0]
            process_type_name = process_type.upper()
            if key_split == process_type_name:
                append_keys.append(key)

        output_data = []

        for key_data in append_keys:
            data_redis = conn.hgetall("{}".format(key_data))
            output_data.append(data_redis)

        return output_data

    @classmethod
    def delete_redis_key_from_storage(cls, redis_key):
        """

        :param redis_key: key for searching redis for data
        :return: it will return default call for function that is executed
        """
        for x in conn.keys():
            if str(redis_key) == str(x):
                conn.delete(redis_key)
                logger_api.info("Key deleted: %s" % redis_key)
        return
