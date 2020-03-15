"""empty message

Revision ID: 2217d6f855fe
Revises: 58d401585cc2
Create Date: 2020-03-15 00:39:32.006823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2217d6f855fe'
down_revision = '58d401585cc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('contents', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    # ### end Alembic commands ###