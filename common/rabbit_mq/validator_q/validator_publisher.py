from kombu import Exchange, Producer, Queue

from common.rabbit_mq.common.const import ValidationEnum
from common.rabbit_mq.connection.connection import conn, channel
from common.logging.setup import logger
from common.redis.core.handle_fail_of_rabit_mq import RedisHandler

exchange = Exchange("{}".format(ValidationEnum.VALIDATION_Q.value), type="direct")

producer = Producer(
    exchange=exchange,
    channel=channel,
    routing_key="{}".format(ValidationEnum.VALIDATION_Q_KEY.value)
)
queue = Queue(
    name="{}".format(ValidationEnum.VALIDATION_Q.value),
    exchange=exchange,
    routing_key="{}".format(ValidationEnum.VALIDATION_Q_KEY.value)
)

queue.maybe_bind(conn)
queue.declare()


def validate_publish_message(company_id, data, type_of_process):
    """
    :param company_id: cloud company_id
    :param data: JSON process
    :param type_of_process:
    :return: JSON of success validation
    """
    if not company_id or company_id is None:
        return {'success': False, 'message': 'Please send company_id.'}
    elif data and len(data) == 0:
        return {'success': False, 'message': 'Data is empty for this request.'}
    elif type_of_process is None:
        return {'success': False, 'message': 'Please send type_of_process.'}
    else:
        return {'success': True, 'message': 'Process added to Q.'}


def publish_robot_validation_data(company_id, data, type_of_process, language, robot_id, publish_message, date):
    """
    :param company_id: company_id
    :param data: JSON process
    :param type_of_process:
    :param language:
    :param robot_id:
    :param publish_message:
    :param date:
    :return: it will return results of success or fail process inserting in Rabbit MQ
    """
    check_data = validate_publish_message(company_id, data, type_of_process)
    if not check_data['success']:
        return check_data

    # Check redis if keys exists
    redis_store = RedisHandler.return_all_data_from_redis_by_key(type_of_process)
    if len(redis_store) > 0:
        for x in redis_store:
            logger.info("Processes in Q")
            redis_key = x['type'] + '_' + x['robot_id'] + '_' + x['company_id']
            RedisHandler.delete_redis_key_from_storage(redis_key)
            producer.publish(x)

    # Process current message
    message = {
        'company_id': company_id,
        'data': data,
        'type': type_of_process,
        'robot_id': robot_id,
        'language': language,
        'publish_message': publish_message,
        'date': date
    }
    logger.info("Processes in Q for database validation.")
    try:
        producer.publish(message, retry=True)
        logger.info("Process published to Q: {}".format(message))
        return {'success': True, 'message': "Published to Q. Your data: {}".format(message)}
    except Exception as e:
        logger.error("Cant publish to validation Q for file validation. Error: {}".format(e))
        logger.info("Calling redis for data store. Data: %s" % message)
        try:
            RedisHandler.set_redis_validation_fail_process(
                process_data=message,
                process_type=type_of_process,
                robot_id=robot_id,
                company_id=company_id
            )
            return {'success': True,
                    'message': "RabbitMQ fail, setting data to redis. Error: {}".format(e)}
        except Exception as e:
            logger.error("Redis error on inserting to storage. Error: {}".format(e))
            return {'success': False,
                    'message': "RabbitMQ fail, setting data to redis. Error: {}".format(e)
                    }

