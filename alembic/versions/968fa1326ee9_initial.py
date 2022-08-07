"""initial

Revision ID: 968fa1326ee9
Revises: 
Create Date: 2022-08-07 14:29:02.343876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '968fa1326ee9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False, comment='User ID'),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True, comment="User's first name"),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True, comment="User's last name"),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True, comment="User's email"),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['user_group.id'], name='user_group_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    # ### end Alembic commands ###
