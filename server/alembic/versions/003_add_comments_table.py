"""添加评论表

Revision ID: 003
Revises: 002
Create Date: 2025-11-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建comments表
    op.create_table(
        'comments',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='评论ID'),
        sa.Column('user_id', sa.BigInteger(), nullable=False, comment='用户ID'),
        sa.Column('target_type', sa.String(length=20), nullable=False, comment='目标类型:poetry,post'),
        sa.Column('target_id', sa.BigInteger(), nullable=False, comment='目标ID'),
        sa.Column('parent_id', sa.BigInteger(), nullable=True, comment='父评论ID（二级评论）'),
        sa.Column('content', sa.Text(), nullable=False, comment='评论内容'),
        sa.Column('like_count', sa.Integer(), server_default='0', nullable=True, comment='点赞数'),
        sa.Column('reply_count', sa.Integer(), server_default='0', nullable=True, comment='回复数'),
        sa.Column('status', sa.SmallInteger(), server_default='1', nullable=True, comment='状态:1正常,2已删除'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True, comment='更新时间'),
        sa.ForeignKeyConstraint(['parent_id'], ['comments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
        comment='评论表'
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_index(op.f('ix_comments_user_id'), 'comments', ['user_id'], unique=False)
    op.create_index(op.f('ix_comments_target_type'), 'comments', ['target_type'], unique=False)
    op.create_index(op.f('ix_comments_target_id'), 'comments', ['target_id'], unique=False)
    op.create_index('ix_comments_target', 'comments', ['target_type', 'target_id'], unique=False)
    op.create_index(op.f('ix_comments_parent_id'), 'comments', ['parent_id'], unique=False)
    op.create_index(op.f('ix_comments_status'), 'comments', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_comments_status'), table_name='comments')
    op.drop_index(op.f('ix_comments_parent_id'), table_name='comments')
    op.drop_index('ix_comments_target', table_name='comments')
    op.drop_index(op.f('ix_comments_target_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_target_type'), table_name='comments')
    op.drop_index(op.f('ix_comments_user_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
