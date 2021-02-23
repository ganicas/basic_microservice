import csv
import datetime
import pytz
from pytz import timezone
from common.logging.setup import logger
from common.rabbit_mq.validator_q.validator_publisher import publish_robot_validation_data
from common.robot_data_handler.robot_data_procesing.data_validator.validator import RobotDataValidator
from database.master_app_database.common.common import get_local_connection_safe
from sqlalchemy import select
from common.mixin.mixin import get_robot_connection_safe, get_local_connection_safe, PreProcessorRobotHandler
from database.master_app_database.models.models import company, robots_machine
from database.robot_database.models.models import master_app_robot, robot_data


class RobotDataProcessing(object):
    def __init__(self, data, validator_type, company_id, robot_id, robot_serial_number, language=None):
        self.data = data
        self.validator_type = validator_type
        self.language = language if language else 'en'
        self.company_id = company_id
        self.robot_id = robot_id
        self.robot_serial_number = robot_serial_number

    def robot_data_formatter(self):
        main_data_structure = []
        for elements in self.data:
            for element in elements:
                date = element['DATUM']
                time = element['VRIJEME']
                dt = datetime.datetime.strptime(date+str(" ")+time, '%Y/%m/%d %H:%M:%S.%f')
                utc_datetime = dt.replace(tzinfo=pytz.timezone('UTC'))
                utc_datetime_str = utc_datetime.strftime('%Y/%m/%d %H:%M:%S.%f')
                main_data_structure.append({
                    'max_intensity': element['IntenzitetMax'],
                    'intensity': element['Intenzitet'],
                    'max_errors': element['MaxBrojGreski'],
                    'errors': element['BrojGreski'],
                    'big_errors_type_1': element['BrojVelikihGreskiTip1'],
                    'big_errors_type_2': element['BrojVelikihGreskiTip2'],
                    'errors_type_1': element['GreskiMaxTip1'],
                    'errors_type_2': element['GreskiMaxTip2'],
                    'errors_counter': element['Broj_Gresaka'],
                    'ok_intensity': element['IntenzitetDobar_1'],
                    'ok_type1': element['Dobar_1'],
                    'datetime': utc_datetime_str,
                    'serial_number': element['serial_number'],
                })
        self.validate_robot_data(data=main_data_structure)

    def validate_robot_data(self, data):
        robot_pre_processor = PreProcessorRobotHandler(
            company_id=self.company_id,
            robot_data=data,
            robot_id=self.robot_id
        )
        generate_robot_data_json_hash = robot_pre_processor.robot_data_json_hash(json_obj=data)
        if generate_robot_data_json_hash:
            success_history, history = robot_pre_processor.check_existing_robot_hash(
                data_hash=generate_robot_data_json_hash
            )
            if success_history:
                logger.info("Robot data already success process: {}".format(history))
            else:
                validator = RobotDataValidator(
                    validator_type=self.validator_type,
                    company_id=self.company_id,
                    language=self.language,
                    robot_data=data,
                    robot_id=self.robot_id
                )
                validator_status = validator.validate_data()
                if validator_status:
                    with get_local_connection_safe() as conn_local:
                        insert_data = {
                            'company_id': self.company_id,
                            'robot_id': self.robot_id,
                            'data': data,
                            'data_hash': generate_robot_data_json_hash
                        }
                        conn_local.execute(robot_data.insert(), insert_data)
                    logger.info("Success validate data and publish to RMQ: {}".format(validator_status))
        else:
            from django.utils import timezone
            logger.info("No data for processing publish to RMQ")
            publish_robot_validation_data(
                company_id=self.company_id,
                data=None,
                type_of_process=self.validator_type,
                language=self.language,
                robot_id=self.robot_id,
                robot_serial_number=self.robot_serial_number,
                publish_message={'working_status': True, 'custom_message': 'no data for processing'},
                date=timezone.now()
            )


def get_robot_for_processing(robot_serial_number):
    """
    This method compare django app robots and robot of this service, same robot_id is alive robots!
    :return:  alive robots
    """
    with get_robot_connection_safe() as conn_master_robot, get_local_connection_safe() as conn_local:
        # Get robot info from master app
        robot_query = select([robots_machine]).where(robots_machine.serial_number == robot_serial_number)
        result = conn_master_robot.execute(robot_query)
        robot_results = [
            {
                'robot_id': int(x.id) if x.id else None,
                'company_id': int(x.company_id) if x.company_id else None,
                'company_name': x.name
            }
            for x in result
        ]
        # Get robot info from local data
        robot_local = select([master_app_robot]).where(master_app_robot.c.serial_number == robot_serial_number)
        run_robot = conn_local.execute(robot_local)
        robot_local_data = [
            {
                'robot_id': int(x.robot_id) if x.robot_id else None,
                'company_id': int(x.company_id) if x.company_id else None,
                'ip_address': x.ip_address,
                'serial_number': x.serial_number,
                'robot_username': x.robot_username,
                'robot_password': x.robot_password
            }
            for x in run_robot.fetchall()
        ]

        alive_robot = []
        if robot_results:
            for robot in robot_results:
                # Filter remote and local robot info
                robot_filter = list(filter(lambda x: x['robot_id'] == robot['robot_id'], robot_local_data))
                if len(robot_filter):
                    alive_robot.append(robot_filter)
        return alive_robot



"""
def get_robot_for_processing():
    with get_robot_connection_safe() as conn_master_robot, get_local_connection_safe() as conn_local:
        # Get robot info from master app
        robot_query = select([robots_machine])
        result = conn_master_robot.execute(robot_query)
        robot_results = [
            {
                'robot_id': int(x.id) if x.id else None,
                'company_id': int(x.company_id) if x.company_id else None,
                'company_name': x.name
            }
            for x in result
        ]
        # Get robot info from local data
        robot_local = select([master_app_robot])
        run_robot = conn_local.execute(robot_local)
        robot_local_data = [
            {
                'robot_id': int(x.robot_id) if x.robot_id else None,
                'company_id': int(x.company_id) if x.company_id else None
            }
            for x in run_robot.fetchall()
        ]

        alive_robot = []
        if robot_results:
            for robot in robot_results:
                # Filter remote and local robot info
                robot_filter = list(filter(lambda x: x['robot_id'] == robot['robot_id'], robot_local_data))
                if len(robot_filter):
                    local_robot_data = select([robot_data])
                    run_robot_data = conn_local.execute(local_robot_data)
                    get_local_robot_data = [
                        {
                            'data': x.data,
                            'robot_id': int(x.robot_id) if x.robot_id else None,
                            'company_id': int(x.company_id) if x.company_id else None,
                            'created_at': x.created_at,
                            'updated_at': x.updated_at
                        }
                        for x in run_robot_data.fetchall()
                    ]
                    # select matched robot info and get robot data
                    robot_data_filter = list(filter(lambda x: x['robot_id'] == robot['robot_id'], get_local_robot_data))
                    if len(robot_data_filter):
                        alive_robot.append(robot_data_filter)
        return alive_robot

"""


if __name__ == "__main__":
    pass