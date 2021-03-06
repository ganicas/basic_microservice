"""Create database

Revision ID: 6ff1091e78be
Revises: 6ca59607f344
Create Date: 2018-11-27 16:32:23.894265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ff1091e78be'
down_revision = '6ca59607f344'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('master_app_robot', sa.Column('ip_address', sa.String(length=20), nullable=True))
    op.add_column('master_app_robot', sa.Column('robot_password', sa.String(length=255), nullable=True))
    op.add_column('master_app_robot', sa.Column('robot_username', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('master_app_robot', 'robot_username')
    op.drop_column('master_app_robot', 'robot_password')
    op.drop_column('master_app_robot', 'ip_address')
    # ### end Alembic commands ###
