"""init models

Revision ID: bedbd670c13d
Revises: 
Create Date: 2024-10-25 23:19:15.498025

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'bedbd670c13d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phoneNumber', sa.String(), nullable=False),
    sa.Column('passwordHash', sa.String(), nullable=False),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.Column('isActive', sa.Boolean(), nullable=False),
    sa.Column('isDeleted', sa.Boolean(), nullable=False),
    sa.Column('createdAt', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updatedAt', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phoneNumber')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_isActive'), 'users', ['isActive'], unique=False)
    op.create_index(op.f('ix_users_isDeleted'), 'users', ['isDeleted'], unique=False)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_role'), table_name='users')
    op.drop_index(op.f('ix_users_isDeleted'), table_name='users')
    op.drop_index(op.f('ix_users_isActive'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###