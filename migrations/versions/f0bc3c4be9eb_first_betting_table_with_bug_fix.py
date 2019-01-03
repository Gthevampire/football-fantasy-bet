"""First betting table with bug fix

Revision ID: f0bc3c4be9eb
Revises: 265c2bf3cb1a
Create Date: 2019-01-03 19:07:57.470148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0bc3c4be9eb'
down_revision = '265c2bf3cb1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('home_goals', sa.Integer(), nullable=True),
    sa.Column('away_goals', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('match',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('home_team_id', sa.Integer(), nullable=True),
    sa.Column('away_team_id', sa.Integer(), nullable=True),
    sa.Column('end_score_id', sa.Integer(), nullable=True),
    sa.Column('extra_score_id', sa.Integer(), nullable=True),
    sa.Column('shootout_score_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['away_team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['end_score_id'], ['score.id'], ),
    sa.ForeignKeyConstraint(['extra_score_id'], ['score.id'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['shootout_score_id'], ['score.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_match_date'), 'match', ['date'], unique=False)
    op.create_table('bet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=True),
    sa.Column('score_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['match.id'], ),
    sa.ForeignKeyConstraint(['score_id'], ['score.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bet')
    op.drop_index(op.f('ix_match_date'), table_name='match')
    op.drop_table('match')
    op.drop_table('team')
    op.drop_table('score')
    # ### end Alembic commands ###