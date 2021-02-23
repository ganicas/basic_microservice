"""Create database

Revision ID: 38570b70f218
Revises: 9d54bfdcc4c7
Create Date: 2019-01-27 20:04:30.783357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38570b70f218'
down_revision = '9d54bfdcc4c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('master_app_robot_notification', sa.Column('notification_id', sa.BigInteger(), nullable=True))
    op.create_index(op.f('ix_master_app_robot_notification_notification_id'), 'master_app_robot_notification', ['notification_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_master_app_robot_notification_notification_id'), table_name='master_app_robot_notification')
    op.drop_column('master_app_robot_notification', 'notification_id')
    # ### end Alembic commands ###