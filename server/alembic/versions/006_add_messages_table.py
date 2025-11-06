"""添加消息表

Revision ID: 006
Revises: 005
Create Date: 2025-11-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '006'
down_revision: Union[str, None] = '005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建messages表
    op.create_table(
        'messages',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='消息ID'),
        sa.Column('user_id', sa.BigInteger(), nullable=False, comment='接收用户ID'),
        sa.Column('type', sa.String(length=20), nullable=False, comment='消息类型'),
        sa.Column('title', sa.String(length=100), nullable=False, comment='消息标题'),
        sa.Column('content', sa.Text(), nullable=True, comment='消息内容'),
        sa.Column('data', sa.JSON(), nullable=True, comment='关联数据'),
        sa.Column('from_user_id', sa.BigInteger(), nullable=True, comment='发送者ID'),
        sa.Column('target_type', sa.String(length=20), nullable=True, comment='目标类型:poetry,post,comment'),
        sa.Column('target_id', sa.BigInteger(), nullable=True, comment='目标ID'),
        sa.Column('is_read', sa.SmallInteger(), server_default='0', nullable=True, comment='是否已读:0未读,1已读'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.Column('read_at', sa.DateTime(), nullable=True, comment='阅读时间'),
        sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
        comment='消息表'
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)
    op.create_index(op.f('ix_messages_user_id'), 'messages', ['user_id'], unique=False)
    op.create_index(op.f('ix_messages_type'), 'messages', ['type'], unique=False)
    op.create_index(op.f('ix_messages_from_user_id'), 'messages', ['from_user_id'], unique=False)
    op.create_index(op.f('ix_messages_is_read'), 'messages', ['is_read'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_messages_is_read'), table_name='messages')
    op.drop_index(op.f('ix_messages_from_user_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_type'), table_name='messages')
    op.drop_index(op.f('ix_messages_user_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')
