from datetime import datetime

from common.logging.setup import logger
from common.mixin.mixin import return_something_from_list
from common.rabbit_mq.validator_q.validator_publisher import publish_robot_validation_data
from common.robot_data_handler.robot_data_procesing.data_validator.validation_const import \
    return_validator_type_based_on_parser, serializer_data, find_key_and_custom_message
import jsonschema
from jsonschema import validate, FormatChecker, Draft4Validator
from operator import itemgetter


class RobotDataValidator(object):
    def __init__(self, validator_type, robot_data, company_id, robot_id, language=None):
        self.validator_type = validator_type
        self.robot_data = robot_data
        self.language = language if language else 'en'
        self.company_id = company_id
        self.robot_id = robot_id

    def return_errors_from_json_schema(self, object_input, error, line):
        count = line
        errors_append = []
        v = Draft4Validator(self.validator_type)
        errors = sorted(v.iter_errors(object_input), key=lambda e: e.schema_path)
        if len(error.context):
            for idx, item in enumerate(error.context):
                vt = return_something_from_list(idx, error.context)
                if len(vt.path) > 0:
                    msg3 = find_key_and_custom_message(vt.path[0], self.language, self.validator_type)
                    if msg3['success']:
                        insert_m = {"record": vt.path[0],
                                    "message": "Line: {}: {}".format(count, msg3['message'])}
                        errors_append.append(insert_m)
                    else:
                        insert_m = {"record": vt.path[0],
                                    "message": "Line: {}: {}".format(count, vt.message)}
                        errors_append.append(insert_m)
                else:
                    msg_extract = return_something_from_list(idx, error.context)
                    error_path = msg_extract.message.split("'")[1]
                    msg3 = find_key_and_custom_message(error_path, self.language, self.validator_type)
                    if msg3['success']:
                        insert_m = {'record': error_path,
                                    'message': 'Line: {}: {}'.format(count, msg3['message'])}
                        errors_append.append(insert_m)
                    else:
                        insert_m = {'record': error_path,
                                    'message': 'Line: {}: {}'.format(count, msg_extract.message)}
                        errors_append.append(insert_m)
            path = None
            for error in errors:
                if len(error.path) > 0:
                    path = error.path[0]
                elif error.validator:
                    path = error.validator
                if path:
                    msg3 = find_key_and_custom_message(path, self.language, self.validator_type)
                    if msg3['success']:
                        insert_m = {"record": path,
                                    "message": "Line: {}: {}".format(count, msg3['message'])}
                        errors_append.append(insert_m)
                    else:
                        insert_m = {"record": path, "message": "Line: {}: {}".format(count, error.message)}
                        errors_append.append(insert_m)
        else:
            path = None
            for error in errors:
                if len(error.path) > 0:
                    path = error.path[0]
                elif error.validator:
                    path = error.validator
                if path:
                    msg3 = find_key_and_custom_message(path, self.language, self.validator_type)
                    if msg3['success']:
                        insert_m = {"record": path,
                                    "message": "Line: {}: {}".format(count, msg3['message'])}
                        errors_append.append(insert_m)
                    else:
                        insert_m = {"record": path, "message": "Line: {}: {}".format(count, error.message)}
                        errors_append.append(insert_m)

        return errors_append

    def validate_data(self):
        get_default_parser = return_validator_type_based_on_parser(self.validator_type)
        output_values = serializer_data(values_data=self.robot_data, parser=get_default_parser)
        output_response = []
        count_line = 1
        logger.info("Start robot data validation, robot_id: {} ".format(self.robot_id))
        for row in output_values:
            count_line += 1
            try:
                validate(row, get_default_parser, format_checker=FormatChecker())
            except jsonschema.exceptions.ValidationError as e:
                output_error = self.return_errors_from_json_schema(object_input=row, error=e, line=count_line)
                for list_item in output_error:
                    output_response.append(list_item)

        logger.info("This is all error of file validation {}: ".format(output_response))
        if len(output_response) > 0:
            unique_len = sorted(output_response, key=itemgetter('record'))
            new_d = []
            for x in unique_len:
                if x not in new_d:
                    new_d.append(x)
            if len(new_d):
                for error in new_d:
                    error_message = error['record'] + '. ' + error['message']
                    logger.info("This is all error of file validation , parse message {}: ".format(error_message))

                return False
        publish_robot_validation_data(
            company_id=self.company_id,
            data=output_values,
            type_of_process=self.validator_type,
            language=self.language,
            robot_id=self.robot_id,
            publish_message={'working_status': True, 'custom_message': 'processed'},
            date=datetime.utcnow()
        )
        logger.info("Success finish data validation: {}".format(self.robot_id))
        return True
