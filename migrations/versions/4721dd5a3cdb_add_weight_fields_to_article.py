"""Add weight fields to article

Revision ID: 4721dd5a3cdb
Revises: d15d5d6e1242
Create Date: 2025-05-06 01:10:14.596682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4721dd5a3cdb'
down_revision = 'd15d5d6e1242'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('weight_real', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('weight_code', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_column('weight_code')
        batch_op.drop_column('weight_real')

    # ### end Alembic commands ###
