from sqlalchemy import exc
from database.robot_database.connection.connection import engine as local_engine
from database.master_app_database.connection.connection import master_app_database_engine
from contextlib import contextmanager
from common.logging.setup import logger


@contextmanager
def get_master_app_connection_safe(*args, **kwds):
    session_cloud = None
    try:
        session_cloud = master_app_database_engine.connect()
        yield session_cloud
    except exc.SQLAlchemyError as e:
        print(e)
        logger.error("Master app connection context manager exception -> {}".format(str(e)))
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


class ConnectionForDatabases(object):
    """
    MASTER APP or Robot database connection class methods.
    """

    @classmethod
    def get_local_connection(cls):
        try:
            session_local = local_engine
            return session_local
        except exc.SQLAlchemyError as e:
            print(e)
            logger.error("Master app connection exception -> {}".format(str(e)))

    @classmethod
    def get_master_app_connection(cls):
        try:
            session_cloud = master_app_database_engine
            return session_cloud
        except exc.SQLAlchemyError as e:
            print(e)
            logger.error("Local connection exception -> {}".format(str(e)))
