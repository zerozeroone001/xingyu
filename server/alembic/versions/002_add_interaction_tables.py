"""添加用户诗词交互表

Revision ID: 002
Revises: 001
Create Date: 2025-11-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建user_poetry_likes表
    op.create_table(
        'user_poetry_likes',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='ID'),
        sa.Column('user_id', sa.BigInteger(), nullable=False, comment='用户ID'),
        sa.Column('poetry_id', sa.BigInteger(), nullable=False, comment='诗词ID'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.ForeignKeyConstraint(['poetry_id'], ['poetries.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_user_poetry_like_user_id'), 'user_poetry_likes', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_poetry_like_poetry_id'), 'user_poetry_likes', ['poetry_id'], unique=False)
    op.create_index('ix_user_poetry_like_unique', 'user_poetry_likes', ['user_id', 'poetry_id'], unique=True)
    op.create_index(op.f('ix_user_poetry_likes_id'), 'user_poetry_likes', ['id'], unique=False)

    # 创建user_poetry_collections表
    op.create_table(
        'user_poetry_collections',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='ID'),
        sa.Column('user_id', sa.BigInteger(), nullable=False, comment='用户ID'),
        sa.Column('poetry_id', sa.BigInteger(), nullable=False, comment='诗词ID'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.ForeignKeyConstraint(['poetry_id'], ['poetries.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_user_poetry_collection_user_id'), 'user_poetry_collections', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_poetry_collection_poetry_id'), 'user_poetry_collections', ['poetry_id'], unique=False)
    op.create_index('ix_user_poetry_collection_unique', 'user_poetry_collections', ['user_id', 'poetry_id'], unique=True)
    op.create_index(op.f('ix_user_poetry_collections_id'), 'user_poetry_collections', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_poetry_collections_id'), table_name='user_poetry_collections')
    op.drop_index('ix_user_poetry_collection_unique', table_name='user_poetry_collections')
    op.drop_index(op.f('ix_user_poetry_collection_poetry_id'), table_name='user_poetry_collections')
    op.drop_index(op.f('ix_user_poetry_collection_user_id'), table_name='user_poetry_collections')
    op.drop_table('user_poetry_collections')

    op.drop_index(op.f('ix_user_poetry_likes_id'), table_name='user_poetry_likes')
    op.drop_index('ix_user_poetry_like_unique', table_name='user_poetry_likes')
    op.drop_index(op.f('ix_user_poetry_like_poetry_id'), table_name='user_poetry_likes')
    op.drop_index(op.f('ix_user_poetry_like_user_id'), table_name='user_poetry_likes')
    op.drop_table('user_poetry_likes')
