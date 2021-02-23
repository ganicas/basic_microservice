"""Create database

Revision ID: 2c6b477638cf
Revises: 38570b70f218
Create Date: 2019-01-27 21:22:16.061437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c6b477638cf'
down_revision = '38570b70f218'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('master_app_robot_notification', sa.Column('email1', sa.String(length=100), nullable=True))
    op.add_column('master_app_robot_notification', sa.Column('email2', sa.String(length=100), nullable=True))
    op.add_column('master_app_robot_notification', sa.Column('email3', sa.String(length=100), nullable=True))
    op.add_column('master_app_robot_notification', sa.Column('email4', sa.String(length=100), nullable=True))
    op.add_column('master_app_robot_notification', sa.Column('email5', sa.String(length=100), nullable=True))
    op.drop_column('master_app_robot_notification', 'email_4')
    op.drop_column('master_app_robot_notification', 'email_3')
    op.drop_column('master_app_robot_notification', 'email_5')
    op.drop_column('master_app_robot_notification', 'email_1')
    op.drop_column('master_app_robot_notification', 'email_2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('master_app_robot_notification', sa.Column('email_2', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('master_app_robot_notification', sa.Column('email_1', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('master_app_robot_notification', sa.Column('email_5', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('master_app_robot_notification', sa.Column('email_3', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('master_app_robot_notification', sa.Column('email_4', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('master_app_robot_notification', 'email5')
    op.drop_column('master_app_robot_notification', 'email4')
    op.drop_column('master_app_robot_notification', 'email3')
    op.drop_column('master_app_robot_notification', 'email2')
    op.drop_column('master_app_robot_notification', 'email1')
    # ### end Alembic commands ###
