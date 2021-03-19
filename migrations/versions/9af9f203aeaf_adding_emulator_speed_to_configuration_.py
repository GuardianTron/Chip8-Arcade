"""Adding emulator speed to configuration settings

Revision ID: 9af9f203aeaf
Revises: d04a716a324d
Create Date: 2021-03-19 00:30:04.934935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9af9f203aeaf'
down_revision = 'd04a716a324d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('control_config', sa.Column('emulator_speed', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('control_config', 'emulator_speed')
    # ### end Alembic commands ###
