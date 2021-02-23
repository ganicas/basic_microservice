import time
from sqlalchemy.sql import select, update
from database.master_app_database.common.common import get_master_app_connection_safe, get_local_connection_safe
from database.master_app_database.models.models import (
    company, device, user_role, product, robots_machine, rescan_robot_machine, robot_notification)
from database.robot_database.models.models import (
    master_app_company, master_app_robot, master_app_robot_rescanning, master_app_robot_notification, robot_data)
from sqlalchemy import func, join, insert, and_


class MasterAppLocalDatabaseSync(object):
    @classmethod
    def query_master_app_company_initial_insert(cls):
        """
        This method make sync company from master app with local robot master_app_company!
        :return: master_app_company update
        """

        with get_master_app_connection_safe() as conn_cloud, get_local_connection_safe() as conn_local:
            company_query = select([company])
            result = conn_cloud.execute(company_query)
            if result:
                company_results = [
                    {
                        'company_id': int(x.id) if x.id else None,
                        'product_id': int(x.product_id) if x.product_id else None,
                        'company_name': x.name
                    }
                    for x in result
                ]

                company_local = select([master_app_company])
                run_company = conn_local.execute(company_local)
                master_app_company_list = []
                company_local_id = [int(x.company_id) for x in run_company.fetchall()]

                for cmp in company_results:
                    if int(cmp['company_id']) not in master_app_company_list:
                        master_app_company_list.append(int(cmp['company_id']))
                    if int(cmp['company_id']) not in company_local_id:
                        ins = master_app_company.insert().values(cmp)
                    else:
                        ins = master_app_company.update().values(cmp).where(
                            master_app_company.c.company_id == int(cmp['company_id']))
                    conn_local.execute(ins)

                if company_local_id:
                    for y in company_local_id:
                        if y not in master_app_company_list:
                            company_local_delete = master_app_company.delete().where(
                                master_app_company.c.company_id == int(y))
                            conn_local.execute(company_local_delete)

        return

    @classmethod
    def query_master_app_robot_initial_insert(cls):
        """
        This method make sync robot from master app with local robot master_app_robot!
        :return: master_app_company update
        """

        with get_master_app_connection_safe() as conn_cloud, get_local_connection_safe() as conn_local:
            robot_query = select([robots_machine])
            result = conn_cloud.execute(robot_query)
            robot_results = [
                {
                    'robot_id': int(x.id) if x.id else None,
                    'product_id': int(x.product_id) if x.product_id else None,
                    'company_id': int(x.company_id) if x.company_id else None,
                    'robot_name': x.name,
                    'ip_address': x.robot_ip_address,
                    'robot_username': x.robot_username,
                    'robot_password': x.robot_password,
                    'serial_number': x.serial_number,
                    'enabled': x.enabled,
                    'active': x.active,
                }
                for x in result
            ]

            company_local = select([master_app_robot])
            run_robot = conn_local.execute(company_local)

            robot_local_id = [int(x.robot_id) for x in run_robot.fetchall()]
            master_app_robot_list = []
            for robot in robot_results:
                if int(robot['robot_id']) not in master_app_robot_list:
                    master_app_robot_list.append(int(robot['robot_id']))
                if int(robot['robot_id']) not in robot_local_id:
                    ins = master_app_robot.insert().values(robot)
                else:
                    ins = master_app_robot.update().values(robot).where(
                        master_app_robot.c.robot_id == int(robot['robot_id']))
                conn_local.execute(ins)

            if robot_local_id:
                for y in robot_local_id:
                    if y not in master_app_robot_list:
                        robot_local_delete = master_app_robot.delete().where(master_app_robot.c.robot_id == int(y))
                        conn_local.execute(robot_local_delete)
        return

    @classmethod
    def query_master_app_robot_rescan(cls):
        with get_master_app_connection_safe() as conn_cloud, get_local_connection_safe() as conn_local:
            robot_query = select([rescan_robot_machine])
            result = conn_cloud.execute(robot_query)
            robot_results = [
                {
                    'robot_id': int(x.robot_id) if x.robot_id else None,
                    'rescan_start': x.start_date,
                    'rescan_end': x.end_date,
                    'activate_rescan': x.activate_rescan,
                    'rescan_status': x.rescan_status,
                }
                for x in result
            ]
            master_app_rescan_list = []
            if robot_results:
                master_app_robot_local = select([master_app_robot_rescanning])
                run_robot = conn_local.execute(master_app_robot_local)
                robot_local_id = [int(x.robot_id) for x in run_robot.fetchall()]
                for rescan in robot_results:
                    if int(rescan['robot_id']) not in master_app_rescan_list:
                        master_app_rescan_list.append(int(rescan['robot_id']))
                    if int(rescan['robot_id']) not in robot_local_id:
                        ins = master_app_robot_rescanning.insert().values(rescan)
                    else:
                        ins = master_app_robot_rescanning.update().values(rescan).where(
                            master_app_robot_rescanning.c.robot_id == int(rescan['robot_id']))
                    conn_local.execute(ins)

                if robot_local_id:
                    for y in robot_local_id:
                        if y not in master_app_rescan_list:
                            robot_local_delete = master_app_robot_rescanning.delete().where(
                                master_app_robot_rescanning.c.robot_id == int(y))
                            conn_local.execute(robot_local_delete)

        return

    @classmethod
    def query_master_app_robot_notification(cls):
        """
        This method make sync robot from master app with local robot master_app_robot!
        :return: master_app_company update
        """

        with get_master_app_connection_safe() as conn_cloud, get_local_connection_safe() as conn_local:
            robot_query = select([robot_notification])
            result = conn_cloud.execute(robot_query)
            notification_results = [
                {
                    'email1': x.email1 if x.email1 else None,
                    'email2': x.email2 if x.email2 else None,
                    'email3': x.email3 if x.email3 else None,
                    'email4': x.email4 if x.email4 else None,
                    'email5': x.email5 if x.email5 else None,
                    'error': x.error,
                    'warning': x.warning,
                    'notification_id': x.id,
                    'info': x.info,
                    'robot_activity': x.robot_activity,
                    'active': x.active,
                }
                for x in result
            ]
            notification_local = select([master_app_robot_notification])
            run_notification = conn_local.execute(notification_local)

            notification_local_id = [int(x.notification_id) for x in run_notification.fetchall()]
            master_app_notification_list = []
            for notification in notification_results:
                if int(notification['notification_id']) not in master_app_notification_list:
                    master_app_notification_list.append(int(notification['notification_id']))
                if int(notification['notification_id']) not in notification_local_id:
                    ins = master_app_robot_notification.insert().values(notification)
                else:
                    ins = master_app_robot_notification.update().values(notification).where(
                        master_app_robot_notification.c.notification_id == int(notification['notification_id']))
                conn_local.execute(ins)

            if notification_local_id:
                for y in notification_local_id:
                    if y not in master_app_notification_list:
                        robot_local_delete = master_app_robot_notification.delete().where(
                            master_app_robot_notification.c.notification_id == int(y))
                        conn_local.execute(robot_local_delete)
        return

    @classmethod
    def return_company_name(cls, company_id):
        with get_local_connection_safe() as conn_local:
            company_local = select([master_app_company]).where(master_app_company.c.company_id == company_id)
            run_q = conn_local.execute(company_local)
            if not run_q.rowcount:
                return ''
            results = run_q.fetchone()
        return results['company_name']

    @classmethod
    def create_new_local_company(cls, company_id, company_name):

        with get_local_connection_safe() as conn_local:

            company_local = select([master_app_company])
            run_company = conn_local.execute(company_local)

            company_local_id = [x.id for x in run_company.fetchall()]

            if int(company_id) in company_local_id:
                return {
                    'status': False,
                    'message': 'Company already exists in local database. Company id: %s' % company_id
                }
            else:
                prepare_ins = {'company_id': int(company_id), 'company_name': company_name}
                ins = master_app_company.insert().values(prepare_ins)
                conn_local.execute(ins)
                return {
                    'status': True,
                    'message': 'Company inserted. Company id: %s' % company_id
                }

    @classmethod
    def check_robot_running_status(cls):
        from datetime import datetime, timedelta
        with get_local_connection_safe() as conn_local:

            get_robot_notification = select([master_app_robot_notification])
            result = conn_local.execute(get_robot_notification)
            notification_results = [
                {
                    'email1': x.email1 if x.email1 else None,
                    'email2': x.email2 if x.email2 else None,
                    'email3': x.email3 if x.email3 else None,
                    'email4': x.email4 if x.email4 else None,
                    'email5': x.email5 if x.email5 else None,
                    'error': x.error,
                    'warning': x.warning,
                    'notification_id': x.id,
                    'info': x.info,
                    'robot_activity': x.robot_activity,
                    'active': x.active,
                }
                for x in result
            ]
            robot_data_local = select([robot_data])
            run_notification = conn_local.execute(robot_data_local)
            robot_data_results = [
                {
                    'company_id': x.company_id if x.company_id else None,
                    'robot_id': x.robot_id if x.robot_id else None,
                    'created_at': x.created_at if x.created_at else None,
                }
                for x in run_notification
            ]
            robot_alarm_list = []
            for notification_item in notification_results:
                email1 = notification_item['email1']
                email2 = notification_item['email2']
                email3 = notification_item['email3']
                email4 = notification_item['email4']
                email5 = notification_item['email5']
                error = notification_item['error']
                warning = notification_item['warning']
                info = notification_item['info']
                active = notification_item['active']
                check_time = notification_item['robot_activity']
                past = datetime.now() - timedelta(minutes=check_time)
                for robot_item in robot_data_results:
                    robot_last_time_status = robot_item['created_at']
                    robot_id = robot_item['robot_id']
                    if past > robot_last_time_status:
                        if active:
                            robot_alarm_list.append({
                                'robot_id': robot_id,
                                "robot_last_time_status": robot_last_time_status,
                                "email_list": [email1, email2, email3, email4, email5],
                                "note": [{'error': error, 'warning': warning, 'info': info}],
                                "status": True
                            })
            if len(robot_alarm_list):
                return robot_alarm_list
            else:
                return [{"status": False}]


def run_sync():
    MasterAppLocalDatabaseSync.query_master_app_company_initial_insert()
    time.sleep(5)
    MasterAppLocalDatabaseSync.query_master_app_robot_initial_insert()
    time.sleep(5)
    MasterAppLocalDatabaseSync.query_master_app_robot_notification()


if __name__ == '__main__':
    """For running sync from command line."""
    run_sync()
