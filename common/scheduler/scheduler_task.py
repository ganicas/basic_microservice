import csv
from apscheduler.scheduler import Scheduler
import time
import json
from sqlalchemy import select
from common.mixin.mixin import get_robot_connection_safe, get_local_connection_safe, PreProcessorRobotHandler, \
    SendNotificationEmail
from common.robot_data_handler.robot_client.client import get_data_from_robot
from common.robot_data_handler.robot_data_procesing.data_processing import RobotDataProcessing, get_robot_for_processing
from database.master_app_database.core.master_app_query import MasterAppLocalDatabaseSync
from database.master_app_database.models.models import company, robots_machine
from database.robot_database.models.models import master_app_robot, robot_data


def run_sync_with_master_app():
    MasterAppLocalDatabaseSync.query_master_app_company_initial_insert()
    time.sleep(1)
    MasterAppLocalDatabaseSync.query_master_app_robot_initial_insert()
    time.sleep(1)
    MasterAppLocalDatabaseSync.query_master_app_robot_rescan()
    time.sleep(1)
    MasterAppLocalDatabaseSync.query_master_app_robot_notification()


def get_robot_serial_number_from_robot_import_data(robot_import_data):
    robot_serial_number = None
    first_row_robot_serial_number = robot_import_data[0]
    for x in first_row_robot_serial_number:
        robot_serial_number = x['serial_number']
    return robot_serial_number


def run_robot_processor():
    # This is some initial implementation
    robot_data_client = get_data_from_robot()
    if len(robot_data_client):
        robot_serial_number = get_robot_serial_number_from_robot_import_data(robot_data_client)
        get_database_robots = get_robot_for_processing(robot_serial_number)

        for robots in get_database_robots:
            time.sleep(2)
            for robot_element in robots:
                company_id = robot_element['company_id']
                robot_id = robot_element['robot_id']
                robot_serial_number = robot_element['serial_number']
                if company_id and robot_id:
                    data_handler = RobotDataProcessing(
                        data=robot_data_client,
                        validator_type='AUTO_INDUSTRY_ROBOT',
                        company_id=company_id,
                        robot_id=robot_id,
                        robot_serial_number=robot_serial_number
                    )
                    data_handler.robot_data_formatter()


def robot_notification():
    notification_status = MasterAppLocalDatabaseSync.check_robot_running_status()
    email_init = SendNotificationEmail(notification_status)
    email_init.prepare_mail()


def main():
    # Start the scheduler
    scheduler = Scheduler()
    scheduler.daemonic = False
    scheduler.start()
    # Schedules job_function to be run once each second
    scheduler.add_interval_job(run_sync_with_master_app,  seconds=5)
    scheduler.add_interval_job(run_robot_processor,  seconds=5)
    scheduler.add_interval_job(robot_notification,  seconds=60)


if __name__ == '__main__':
    main()
