"""empty message

Revision ID: 1abfecb699b1
Revises: 6fd7484cbd19
Create Date: 2022-04-02 10:07:43.235031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1abfecb699b1'
down_revision = '6fd7484cbd19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transfer', 'player_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('transfer', 'origin_team_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('transfer', 'destination_team_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transfer', 'destination_team_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('transfer', 'origin_team_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('transfer', 'player_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
