"""empty message

Revision ID: 3310384132c3
Revises: fa518dd7c8ca
Create Date: 2022-07-06 15:34:59.743215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3310384132c3'
down_revision = 'fa518dd7c8ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('event_parent_event_id_fkey', 'event', type_='foreignkey')
    op.drop_column('event', 'parent_event_id')
    op.drop_column('event', 'first_occurrence')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('first_occurrence', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('event', sa.Column('parent_event_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('event_parent_event_id_fkey', 'event', 'event', ['parent_event_id'], ['id'])
    # ### end Alembic commands ###
