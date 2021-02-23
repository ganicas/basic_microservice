from common.urls.urls_file import robot_database_connection
from sqlalchemy import create_engine

from database.robot_database.models.models import metadata

engine = create_engine(robot_database_connection, convert_unicode=True, echo=False, pool_size=20, max_overflow=100)
metadata.create_all(engine)
