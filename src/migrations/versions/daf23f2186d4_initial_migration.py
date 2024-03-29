"""Initial migration.

Revision ID: daf23f2186d4
Revises: 
Create Date: 2023-06-10 20:15:21.914780

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'daf23f2186d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permissions',
    sa.Column('permission', sa.String(length=80), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('permission')
    )
    op.create_table('roles',
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('is_superuser', sa.BOOLEAN(), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('history',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('ip', postgresql.INET(), nullable=True),
    sa.Column('device_id', sa.String(length=120), nullable=True),
    sa.Column('user_agent', sa.String(length=300), nullable=True),
    sa.Column('login_time', sa.TIMESTAMP(), nullable=False),
    sa.Column('user_device_type', sa.String(length=40), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'user_device_type'),
    sa.UniqueConstraint('id', 'user_device_type'),
    postgresql_partition_by='LIST (user_device_type)'
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "history_smart" PARTITION OF "history" FOR VALUES IN ('smart')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "history_mobile" PARTITION OF "history" FOR VALUES IN ('mobile')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "history_web" PARTITION OF "history" FOR VALUES IN ('web')"""
    )
    op.create_table('roles_permissions',
    sa.Column('permission_id', sa.UUID(), nullable=False),
    sa.Column('role_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('permission_id', 'role_id')
    )
    op.create_table('social_accounts',
    sa.Column('social_id', sa.String(length=200), nullable=False),
    sa.Column('social_name', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('social_id')
    )
    op.create_table('users_roles',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('role_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles')
    op.drop_table('social_accounts')
    op.drop_table('roles_permissions')
    op.execute(
        """
                DROP TABLE IF EXISTS "history_smart";
                DROP TABLE IF EXISTS "history_mobile";
                DROP TABLE IF  EXISTS "history_web";"""
    )
    op.drop_table('history')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('permissions')
    # ### end Alembic commands ###
