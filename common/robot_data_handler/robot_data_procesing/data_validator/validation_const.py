from enum import Enum

from common.logging.setup import logger


class EnumValidationError(Enum):
    MAX_INTENSITY_MESSAGE = {
        "en": "max_intensity field must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    INTENSITY_ERROR_MESSAGE = {
        "en": "intensity field must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    MAX_ERRORS_MESSAGE = {
        "en": "max_errors field must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    ERRORS_MESSAGE = {
        "en": "errors field must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    BIG_ERRORS_TYPE_1_MESSAGE = {
        "en": "big_errors_type_1 must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    BIG_ERRORS_TYPE_2_MESSAGE = {
        "en": "big_errors_type_2 must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    ERRORS_TYPE_1_MESSAGE = {
        "en": "errors_type_1  must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    ERRORS_TYPE_2_MESSAGE = {
        "en": "errors_type_1 must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    ERRORS_COUNTER_MESSAGE = {
        "en": "errors_counter must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    OK_INTENSITY_MESSAGE = {
        "en": "ok_intensity must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    OK_TYPE_1_MESSAGE = {
        "en": "ok_type1 must be integer!",
        "de": "",
        "it": "",
        "fr": ""
    }
    DATETIME_MESSAGE = {
        "en": "datetime must be datetime string in format '%Y/%m/%d %H:%M:%S.%f'",
        "de": "",
        "it": "",
        "fr": ""
    }


RobotDataParser = {
    'type': 'object',
    'properties': {
        "max_intensity": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "intensity": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "max_errors": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "errors": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "big_errors_type_1": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "big_errors_type_2": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "errors_type_1": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "errors_type_2": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "errors_counter": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "ok_intensity": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "ok_type1": {
            'type': 'string',
            'maxLength': 32,
            "minLength": 1
        },
        "datetime": {
            'type': 'string',
            'maxLength': 32,
        },

    },
    'custom_valid_fields': {
        'max_intensity': int,
        'intensity': float,
        'max_errors': int,
        'errors': int,
        'big_errors_type_1': int,
        'big_errors_type_2': int,
        'errors_type_1': int,
        'errors_type_2': int,
        'errors_counter': int,
        'ok_intensity': int,
        'ok_type1': int,
        'datetime': str,
    },
    'required': [
        'max_intensity', 'intensity', 'max_errors', 'errors', 'big_errors_type_1', 'big_errors_type_2', 'errors_type_1',
        'errors_type_2', 'errors_counter', 'ok_intensity', 'ok_type1', 'datetime'
    ],
    'main_fields': [
        'max_intensity', 'intensity', 'max_errors', 'errors', 'big_errors_type_1', 'big_errors_type_2', 'errors_type_1',
        'errors_type_2', 'errors_counter', 'ok_intensity', 'ok_type1', 'datetime'
    ],
    'all_fields': [
        'max_intensity', 'intensity', 'max_errors', 'errors', 'big_errors_type_1', 'big_errors_type_2', 'errors_type_1',
        'errors_type_2', 'errors_counter', 'ok_intensity', 'ok_type1', 'datetime'
    ],
    'custom_message': [{
        'max_intensity': {
            'message': EnumValidationError.MAX_INTENSITY_MESSAGE.value
        },
        'intensity': {
            'message': EnumValidationError.INTENSITY_ERROR_MESSAGE.value
        },
        'max_errors': {
            'message': EnumValidationError.MAX_ERRORS_MESSAGE.value
        },
        'errors': {
            'message': EnumValidationError.ERRORS_MESSAGE.value
        },
        'big_errors_type_1': {
            'message': EnumValidationError.BIG_ERRORS_TYPE_1_MESSAGE.value
        },
        'big_errors_type_2': {
            'message': EnumValidationError.BIG_ERRORS_TYPE_2_MESSAGE.value
        },
        'errors_type_1': {
            'message': EnumValidationError.ERRORS_TYPE_1_MESSAGE.value
        },
        'errors_type_2': {
            'message': EnumValidationError.ERRORS_TYPE_2_MESSAGE.value
        },
        'errors_counter': {
            'message': EnumValidationError.ERRORS_COUNTER_MESSAGE.value
        },
        'ok_intensity': {
            'message': EnumValidationError.OK_INTENSITY_MESSAGE.value
        },
        'ok_type1': {
            'message': EnumValidationError.OK_TYPE_1_MESSAGE.value
        },
        'datetime': {
            'message': EnumValidationError.DATETIME_MESSAGE.value
        }
    }]
}


class ImportType(Enum):
    AUTO_INDUSTRY_ROBOT = {
        'id': 0,
        'def': RobotDataParser,
        'active': True,
        'order': 0,
        'capitalised_name': 'AUTO_INDUSTRY_ROBOT',
    }


def return_validator_type_based_on_parser(validator_type):
    """
    :param validator_type: location, machine, machine_type, regions
    :return: json schema validation type
    """
    for i_type in ImportType:
        if validator_type == i_type.value.get('id') or validator_type == i_type.name:
            return i_type.value['def']


def return_variable_type(input_data):

    if input_data is not None:
        value_type= input_data
        var_type = type(value_type)
        variable_changed = value_type
        if var_type.__name__ == 'int':
            return '{}'.format(int(variable_changed))
        elif var_type.__name__ == 'float':
            spl = str(variable_changed).split('.')
            if int(spl[1]) == 0:
                return '{}'.format(round(float(variable_changed)))
            else:
                return '{}'.format(float(variable_changed))
        elif var_type.__name__ == 'str':
            if variable_changed.lstrip('-').replace('.', '', 1).isdigit():
                z = float(variable_changed)
                c = int(variable_changed.replace('.', '', 1))
                if z != c:
                    spl = str(variable_changed).split('.')
                    if int(spl[1]) == 0:
                        return '{}'.format(round(float(variable_changed)))
                    else:
                        return '{}'.format(float(variable_changed))
                else:
                    return '{}'.format(str(variable_changed))
            else:
                if len(variable_changed) > 0:
                    return '%s' % variable_changed.rstrip()
                else:
                    return None
        elif variable_changed.lower() == 'true':
            return True
        elif variable_changed.lower() == 'false':
            return False
        else:
            return None
    else:
        return None


def serializer_data(values_data, parser):

    parser_json = parser['custom_valid_fields']
    serializer_out = []
    for row in values_data:
        out_row = {}
        for key, val in row.items():
            # Find key
            if len(key):
                try:

                    current_value = return_variable_type(val.rstrip().lstrip())
                    check_key = parser_json.get(key, None)
                except Exception as e:
                    logger.error("Error on serializer_data robot data: {}".format(e))
                if check_key:
                    if current_value and check_key:
                        if check_key.__name__ == 'str':
                            out_row[key] = current_value
                        elif check_key.__name__ == 'int':
                            out_row[key] = current_value
                        elif check_key.__name__ == 'float':
                            out_row[key] = current_value
                    elif not current_value and check_key:
                        if check_key.__name__ == 'str':
                                out_row[key] = None
                        elif check_key.__name__ == 'int':
                            out_row[key] = None
                        elif check_key.__name__ == 'float':
                            out_row[key] = None
        if out_row:
            serializer_out.append(out_row)
        else:
            continue
    return serializer_out


def find_key_and_custom_message(key_in, language, parser):
    """

    :param key_in: specific field of import type
    :param language: desired language for message
    :param parser: json schema validation type
    :return: message on selected language
    """
    key_find = any('%s' % key_in in x for x in parser['custom_message'])
    if key_find:
        msg = parser['custom_message'][0][key_in].get('message', None)
        return {'success': True, 'message': msg[language]}
    else:

        return {'success': False, 'message': ''}
