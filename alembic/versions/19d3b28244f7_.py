"""empty message

Revision ID: 19d3b28244f7
Revises: 1abfecb699b1
Create Date: 2022-04-02 10:08:49.908014

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from server.models.match_event import EventType

revision = '19d3b28244f7'
down_revision = '1abfecb699b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tournament',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_day', sa.Date(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tournament_id'), 'tournament', ['id'], unique=False)
    op.create_table('match',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('tournament_id', sa.Integer(), nullable=False),
    sa.Column('team_1_id', sa.Integer(), nullable=False),
    sa.Column('team_2_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_1_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['team_2_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournament.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_match_id'), 'match', ['id'], unique=False)
    op.create_table('tournament_teams',
    sa.Column('tournament_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournament.id'], )
    )
    op.create_table('match_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('event_type', sqlalchemy_utils.types.choice.ChoiceType(EventType, impl=sa.Integer()), nullable=True),
    sa.Column('string_value', sa.String(), nullable=True),
    sa.Column('integer_value', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['match.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_match_event_id'), 'match_event', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_match_event_id'), table_name='match_event')
    op.drop_table('match_event')
    op.drop_table('tournament_teams')
    op.drop_index(op.f('ix_match_id'), table_name='match')
    op.drop_table('match')
    op.drop_index(op.f('ix_tournament_id'), table_name='tournament')
    op.drop_table('tournament')
    # ### end Alembic commands ###
