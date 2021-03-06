"""Adding configuration table which holds key_code configuration object

Revision ID: 8c587092fed4
Revises: 9fada260312e
Create Date: 2021-03-05 18:12:57.587647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c587092fed4'
down_revision = '9fada260312e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('control_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('key_mapping', sa.PickleType(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('control_config')
    # ### end Alembic commands ###