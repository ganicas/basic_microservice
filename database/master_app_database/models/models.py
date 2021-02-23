
"""

    Cloud models referent by normalize name.

"""
from database.master_app_database.connection.connection import Base

company = Base.classes.administration_companies
custom_user = Base.classes.administration_customuser
product = Base.classes.administration_product
user_role = Base.classes.administration_userroletemplates
device = Base.classes.administration_device
robots_machine = Base.classes.robots_machine
rescan_robot_machine = Base.classes.administration_rescan_robot_machine
robot_notification = Base.classes.administration_notification
