"""empty message

Revision ID: ef931983f95d
Revises: bef4a9bdbeca
Create Date: 2020-06-14 22:19:41.229293

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ef931983f95d'
down_revision = 'bef4a9bdbeca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'nrBowling')
    op.drop_column('user', 'nrDarts')
    op.drop_column('user', 'nrPuncte')
    op.drop_column('user', 'minuteDarts')
    op.drop_column('user', 'minuteTotal')
    op.drop_column('user', 'nrBiliard')
    op.drop_column('user', 'minuteBiliard')
    op.drop_column('user', 'minuteBowling')
    op.drop_column('user', 'nrTotal')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('nrTotal', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('minuteBowling', mysql.FLOAT(), nullable=True))
    op.add_column('user', sa.Column('minuteBiliard', mysql.FLOAT(), nullable=True))
    op.add_column('user', sa.Column('nrBiliard', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('minuteTotal', mysql.FLOAT(), nullable=True))
    op.add_column('user', sa.Column('minuteDarts', mysql.FLOAT(), nullable=True))
    op.add_column('user', sa.Column('nrPuncte', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('nrDarts', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('nrBowling', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###