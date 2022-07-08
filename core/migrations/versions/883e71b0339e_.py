"""empty message

Revision ID: 883e71b0339e
Revises: 3310384132c3
Create Date: 2022-07-08 12:45:29.927253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '883e71b0339e'
down_revision = '3310384132c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'recurrency_rule',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.drop_column('recurrency_meta', 'four_weekly')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recurrency_meta', sa.Column('four_weekly', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.alter_column('event', 'recurrency_rule',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=30),
               existing_nullable=True)
    # ### end Alembic commands ###
