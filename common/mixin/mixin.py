from contextlib import contextmanager
from sqlalchemy import exc
from database.robot_database.connection.connection import engine as local_engine
from common.logging.setup import logger
from database.master_app_database.connection.connection import master_app_database_engine
import json
from sqlalchemy import desc, and_, func, true, delete, asc
from sqlalchemy.sql import insert, select, update

from database.robot_database.models.models import robot_data
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def return_something_from_list(inc, list_in):
    return list_in[inc]


@contextmanager
def get_robot_connection_safe(*args, **kwds):
    session_cloud = None
    try:
        session_cloud = master_app_database_engine.connect()
        yield session_cloud
    except exc.SQLAlchemyError as e:
        print(e)
        logger.error("Cloud connection context manager exception -> {}".format(str(e)))
    finally:
        if session_cloud:
            session_cloud.close()


@contextmanager
def get_local_connection_safe(*args, **kwds):
    session_local = None
    try:
        session_local = local_engine.connect()
        yield session_local
    except exc.SQLAlchemyError as e:
        print(e)
        logger.error("Local connection context manager exception -> {}".format(str(e)))
    finally:
        if session_local:
            session_local.close()


class PreProcessorRobotHandler(object):
    def __init__(self, company_id, robot_id, robot_data):
        self.company_id = company_id
        self.robot_id = robot_id
        self.robot_data = robot_data

    @staticmethod
    def robot_data_json_hash(json_obj):
        import hashlib
        unicode_object = json.dumps(json_obj, sort_keys=True)
        json_hash = hashlib.sha256(str(unicode_object).encode('utf-8')).hexdigest()
        return json_hash

    def robot_redis_handler(self):
        pass

    def check_existing_robot_hash(self, data_hash):
        with get_local_connection_safe() as conn_local:
            robot_query = select([robot_data]).where(and_(
                robot_data.c.company_id == self.company_id,
                robot_data.c.robot_id == self.robot_id,
                robot_data.c.data_hash == data_hash
            ))
            result = conn_local.execute(robot_query)

        return result.rowcount > 0, result.first()

    def check_robot_data_exist(self):
        with get_local_connection_safe() as conn_local:
            robot_query = select([robot_data]).where(and_(
                robot_data.c.company_id == self.company_id,
                robot_data.c.robot_id == self.robot_id,
            ))
            result = conn_local.execute(robot_query)
        return result.rowcount > 0, result


def send_mail(username, password, from_addr, to_addrs, msg):
    print(username, password, from_addr, to_addrs, msg)
    server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()


class SendNotificationEmail(object):
    def __init__(self, init_data):
        self.init_data = init_data
        self.from_address = "proel.design9@yahoo.com"
        self.username = "proel.design9@yahoo.com"
        self.password = "protondesign359"

    def prepare_mail(self):

        html = """Notification email, please check your robot!"""
        if self.init_data[0]['status']:
            robot_list = [x['robot_id'] for x in self.init_data]
            robot_list = set(robot_list)
            if len(robot_list):
                html = "Notification email, please check your robot id: {}. " \
                       "The robot machine currently is not active!".format(robot_list)

            for item in self.init_data:
                status = item['status']
                if status:
                    emails = item['email_list']
                    for email in emails:
                        if email:
                            msg = MIMEMultipart()
                            msg['Subject'] = 'Robot machine Notification'
                            msg['From'] = self.from_address
                            msg['To'] = email

                            # Attach HTML to the email
                            body = MIMEText(html, 'html')
                            msg.attach(body)

                            try:
                                send_mail(self.username, self.password, self.from_address, email, msg)
                                print("Email successfully sent to")
                            except smtplib.SMTPAuthenticationError as e:
                                print('SMTPAuthenticationError', e)
