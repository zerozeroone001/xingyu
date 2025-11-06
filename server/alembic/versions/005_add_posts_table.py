"""添加广场内容表

Revision ID: 005
Revises: 004
Create Date: 2025-11-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建posts表
    op.create_table(
        'posts',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='内容ID'),
        sa.Column('user_id', sa.BigInteger(), nullable=False, comment='用户ID'),
        sa.Column('content', sa.Text(), nullable=False, comment='内容'),
        sa.Column('images', sa.JSON(), nullable=True, comment='图片URLs（JSON数组）'),
        sa.Column('tags', sa.JSON(), nullable=True, comment='标签（JSON数组）'),
        sa.Column('poetry_id', sa.BigInteger(), nullable=True, comment='关联诗词ID'),
        sa.Column('type', sa.String(length=20), server_default='original', nullable=True, comment='类型:original原创,share分享'),
        sa.Column('like_count', sa.Integer(), server_default='0', nullable=True, comment='点赞数'),
        sa.Column('comment_count', sa.Integer(), server_default='0', nullable=True, comment='评论数'),
        sa.Column('collect_count', sa.Integer(), server_default='0', nullable=True, comment='收藏数'),
        sa.Column('view_count', sa.Integer(), server_default='0', nullable=True, comment='浏览数'),
        sa.Column('status', sa.SmallInteger(), server_default='1', nullable=True, comment='状态:1已发布,2草稿,3已删除'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True, comment='更新时间'),
        sa.ForeignKeyConstraint(['poetry_id'], ['poetries.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
        comment='广场内容表'
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.create_index(op.f('ix_posts_user_id'), 'posts', ['user_id'], unique=False)
    op.create_index(op.f('ix_posts_poetry_id'), 'posts', ['poetry_id'], unique=False)
    op.create_index(op.f('ix_posts_type'), 'posts', ['type'], unique=False)
    op.create_index(op.f('ix_posts_status'), 'posts', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_posts_status'), table_name='posts')
    op.drop_index(op.f('ix_posts_type'), table_name='posts')
    op.drop_index(op.f('ix_posts_poetry_id'), table_name='posts')
    op.drop_index(op.f('ix_posts_user_id'), table_name='posts')
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('posts')
