"""empty message

Revision ID: 3bc71c7e1ca6
Revises: d38bd0bd3004
Create Date: 2020-06-13 13:49:04.228628

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3bc71c7e1ca6'
down_revision = 'd38bd0bd3004'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('biliard', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('bowling', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('darts', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('persons_nr', sa.Integer(), nullable=True))
    op.drop_constraint('task_ibfk_1', 'task', type_='foreignkey')
    op.drop_constraint('task_ibfk_2', 'task', type_='foreignkey')
    op.drop_column('task', 'assigned_user_id')
    op.drop_column('task', 'label_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('label_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('task', sa.Column('assigned_user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('task_ibfk_2', 'task', 'label', ['label_id'], ['id'])
    op.create_foreign_key('task_ibfk_1', 'task', 'user', ['assigned_user_id'], ['id'])
    op.drop_column('task', 'persons_nr')
    op.drop_column('task', 'darts')
    op.drop_column('task', 'bowling')
    op.drop_column('task', 'biliard')
    # ### end Alembic commands ###