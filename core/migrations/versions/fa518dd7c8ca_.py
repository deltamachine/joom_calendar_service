"""empty message

Revision ID: fa518dd7c8ca
Revises: 64b9d415740e
Create Date: 2022-07-06 15:32:53.568144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa518dd7c8ca'
down_revision = '64b9d415740e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association',
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('recurrency_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_occurrence', sa.DateTime(), nullable=True),
    sa.Column('last_occurrence', sa.DateTime(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('daily', sa.Boolean(), nullable=True),
    sa.Column('yearly', sa.Boolean(), nullable=True),
    sa.Column('weekly', sa.Boolean(), nullable=True),
    sa.Column('four_weekly', sa.Boolean(), nullable=True),
    sa.Column('monthly', sa.Boolean(), nullable=True),
    sa.Column('interval', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recurrency_meta_id'), 'recurrency_meta', ['id'], unique=False)
    op.add_column('event', sa.Column('parent_event_id', sa.Integer(), nullable=True))
    op.add_column('event', sa.Column('first_occurrence', sa.Boolean(), nullable=True))
    op.add_column('event', sa.Column('recurrency_rule', sa.String(length=30), nullable=True))
    op.create_foreign_key(None, 'event', 'event', ['parent_event_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_column('event', 'recurrency_rule')
    op.drop_column('event', 'first_occurrence')
    op.drop_column('event', 'parent_event_id')
    op.drop_index(op.f('ix_recurrency_meta_id'), table_name='recurrency_meta')
    op.drop_table('recurrency_meta')
    op.drop_table('association')
    # ### end Alembic commands ###