from sqlalchemy import func, text, Date
from sqlalchemy import Table, Integer, String, MetaData, ForeignKey, JSON, DateTime, BigInteger, Boolean, Column


metadata = MetaData()

master_app_company = Table(
    'master_app_company', metadata,
    Column('id', BigInteger, primary_key=True, index=True, autoincrement=True),
    Column('company_id', Integer, index=True, unique=True),
    Column('product_id', Integer, index=True),
    Column('product_name', String(length=255), nullable=True),
    Column('company_name', String(length=255), nullable=True),
    Column('created_at', DateTime, server_default=func.now()),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
)

master_app_robot = Table(
    'master_app_robot', metadata,
    Column('id', BigInteger, primary_key=True, index=True, autoincrement=True),
    Column('robot_id', Integer, index=True, unique=True),
    Column('product_id', Integer, index=True),
    Column('company_id', Integer, index=True),
    Column('active', Boolean, default=False),
    Column('enabled', Boolean, default=False),
    Column('serial_number', String(length=255), nullable=True),
    Column('ip_address', String(length=20), nullable=True),
    Column('robot_username', String(length=255), nullable=True),
    Column('robot_password', String(length=255), nullable=True),
    Column('robot_name', String(length=255), nullable=True),
    Column('created_at', DateTime, server_default=func.now()),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
)


robot_data = Table(
    'robot_data', metadata,
    Column('id', BigInteger, primary_key=True, index=True, autoincrement=True),
    Column('company_id', Integer, ForeignKey('master_app_company.company_id'), nullable=False, index=True),
    Column('robot_id', Integer, ForeignKey('master_app_robot.robot_id', ondelete="CASCADE"), nullable=False, index=True),
    Column('created_at', DateTime, server_default=func.now(), index=True),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
    Column('data_hash', String(length=255), nullable=False, index=True),
    Column('data', JSON, nullable=False),
)


master_app_robot_rescanning = Table(
    'master_app_robot_rescanning', metadata,
    Column('id', BigInteger, primary_key=True, index=True, autoincrement=True),
    Column('robot_id', Integer, ForeignKey('master_app_robot.robot_id', ondelete="CASCADE"), nullable=False, index=True),
    Column('created_at', DateTime, server_default=func.now(), index=True),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
    Column('rescan_start', DateTime),
    Column('rescan_end', DateTime),
    Column('activate_rescan', Boolean, default=False),
    Column('rescan_status', Boolean, default=False),
)


master_app_robot_notification = Table(
    'master_app_robot_notification', metadata,
    Column('id', BigInteger, primary_key=True, index=True, autoincrement=True),
    Column('notification_id', BigInteger, index=True),
    Column('email1', String(length=100), nullable=True),
    Column('email2', String(length=100), nullable=True),
    Column('email3', String(length=100), nullable=True),
    Column('email4', String(length=100), nullable=True),
    Column('email5', String(length=100), nullable=True),
    Column('error', Boolean, default=False),
    Column('warning', Boolean, default=False),
    Column('info', Boolean, default=False),
    Column('robot_activity', Integer),
    Column('active', Boolean, default=False),
    Column('created_at', DateTime, server_default=func.now(), index=True),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
)

