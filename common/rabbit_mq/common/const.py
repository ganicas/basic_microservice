from enum import Enum


class ValidationEnum(Enum):
    VALIDATION_Q = "robot_data_validator"
    VALIDATION_Q_KEY = "robot_data_validator_key"
    DATABASE_Q = "database_message"
    DATABASE_Q_KEY = "database_json"
    VALIDATION_FILE_API_Q = "validator_api"
    VALIDATION_Q_FILE_KEY = "validator_api_json"

    CUSTOM_PUBLISHER = "custom_q"
    CUSTOM_Q_PUBLISHER = "custom_q_publisher"

    EXPORT_PUBLISHER = "export_publisher"
    EXPORT_Q_PUBLISHER = "export_q_publisher"