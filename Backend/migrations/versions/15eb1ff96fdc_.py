"""empty message

Revision ID: 15eb1ff96fdc
Revises: 82f56bc66652
Create Date: 2020-02-28 14:59:24.710883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15eb1ff96fdc'
down_revision = '82f56bc66652'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_task', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_task'], ['task.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
