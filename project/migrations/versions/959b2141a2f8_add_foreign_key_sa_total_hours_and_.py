"""add foreign key sa total_hours and total_overtime

Revision ID: 959b2141a2f8
Revises: 4ba0a4415f68
Create Date: 2023-05-27 11:50:01.487657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '959b2141a2f8'
down_revision = '4ba0a4415f68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pay_roll', schema=None) as batch_op:
        batch_op.add_column(sa.Column('attendance_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'attendance', ['attendance_id'], ['attendance_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pay_roll', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('attendance_id')

    # ### end Alembic commands ###