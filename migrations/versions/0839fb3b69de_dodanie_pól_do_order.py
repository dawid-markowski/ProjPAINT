"""dodanie pól do Order

Revision ID: 0839fb3b69de
Revises: d8d8d08be98c
Create Date: 2025-01-11 12:55:07.638439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0839fb3b69de'
down_revision = 'd8d8d08be98c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DELETE FROM orders')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('city', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('postal_code', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('postal_code')
        batch_op.drop_column('city')
        batch_op.drop_column('address')

    # ### end Alembic commands ###
