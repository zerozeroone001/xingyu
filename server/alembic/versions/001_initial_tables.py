"""初始化数据库表

Revision ID: 001
Revises:
Create Date: 2025-11-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建authors表
    op.create_table(
        'authors',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='作者ID'),
        sa.Column('name', sa.String(length=50), nullable=False, comment='姓名'),
        sa.Column('dynasty', sa.String(length=50), nullable=True, comment='朝代'),
        sa.Column('intro', sa.Text(), nullable=True, comment='简介'),
        sa.Column('avatar', sa.String(length=500), nullable=True, comment='头像'),
        sa.Column('birth_year', sa.Integer(), nullable=True, comment='出生年份'),
        sa.Column('death_year', sa.Integer(), nullable=True, comment='逝世年份'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_authors_id'), 'authors', ['id'], unique=False)
    op.create_index(op.f('ix_authors_name'), 'authors', ['name'], unique=False)
    op.create_index(op.f('ix_authors_dynasty'), 'authors', ['dynasty'], unique=False)

    # 创建users表
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='用户ID'),
        sa.Column('openid', sa.String(length=100), nullable=True, comment='微信openid'),
        sa.Column('unionid', sa.String(length=100), nullable=True, comment='微信unionid'),
        sa.Column('username', sa.String(length=50), nullable=True, comment='用户名'),
        sa.Column('password', sa.String(length=255), nullable=True, comment='密码(bcrypt加密)'),
        sa.Column('nickname', sa.String(length=50), nullable=False, comment='昵称'),
        sa.Column('avatar', sa.String(length=500), nullable=True, comment='头像URL'),
        sa.Column('phone', sa.String(length=20), nullable=True, comment='手机号'),
        sa.Column('gender', sa.SmallInteger(), nullable=True, comment='性别:0未知,1男,2女'),
        sa.Column('intro', sa.String(length=500), nullable=True, comment='个人简介'),
        sa.Column('level', sa.Integer(), nullable=True, comment='用户等级'),
        sa.Column('exp', sa.Integer(), nullable=True, comment='经验值'),
        sa.Column('status', sa.SmallInteger(), nullable=True, comment='状态:1正常,2封禁'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True, comment='更新时间'),
        sa.Column('last_login_at', sa.DateTime(), nullable=True, comment='最后登录时间'),
        sa.PrimaryKeyConstraint('id'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_openid'), 'users', ['openid'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=False)
    op.create_index(op.f('ix_users_status'), 'users', ['status'], unique=False)

    # 创建poetries表
    op.create_table(
        'poetries',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='诗词ID'),
        sa.Column('title', sa.String(length=100), nullable=False, comment='标题'),
        sa.Column('content', sa.Text(), nullable=False, comment='内容'),
        sa.Column('author_id', sa.BigInteger(), nullable=True, comment='作者ID'),
        sa.Column('dynasty', sa.String(length=50), nullable=True, comment='朝代'),
        sa.Column('type', sa.String(length=50), nullable=True, comment='类型:绝句,律诗,词等'),
        sa.Column('tags', sa.JSON(), nullable=True, comment='标签'),
        sa.Column('translation', sa.Text(), nullable=True, comment='翻译'),
        sa.Column('annotation', sa.Text(), nullable=True, comment='注释'),
        sa.Column('appreciation', sa.Text(), nullable=True, comment='赏析'),
        sa.Column('background', sa.Text(), nullable=True, comment='创作背景'),
        sa.Column('read_count', sa.Integer(), nullable=True, comment='阅读数'),
        sa.Column('like_count', sa.Integer(), nullable=True, comment='点赞数'),
        sa.Column('comment_count', sa.Integer(), nullable=True, comment='评论数'),
        sa.Column('collect_count', sa.Integer(), nullable=True, comment='收藏数'),
        sa.Column('status', sa.SmallInteger(), nullable=True, comment='状态:1已发布,2草稿,3已删除'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True, comment='更新时间'),
        sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_poetries_id'), 'poetries', ['id'], unique=False)
    op.create_index(op.f('ix_poetries_title'), 'poetries', ['title'], unique=False)
    op.create_index(op.f('ix_poetries_author_id'), 'poetries', ['author_id'], unique=False)
    op.create_index(op.f('ix_poetries_dynasty'), 'poetries', ['dynasty'], unique=False)
    op.create_index(op.f('ix_poetries_type'), 'poetries', ['type'], unique=False)
    op.create_index(op.f('ix_poetries_status'), 'poetries', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_poetries_status'), table_name='poetries')
    op.drop_index(op.f('ix_poetries_type'), table_name='poetries')
    op.drop_index(op.f('ix_poetries_dynasty'), table_name='poetries')
    op.drop_index(op.f('ix_poetries_author_id'), table_name='poetries')
    op.drop_index(op.f('ix_poetries_title'), table_name='poetries')
    op.drop_index(op.f('ix_poetries_id'), table_name='poetries')
    op.drop_table('poetries')

    op.drop_index(op.f('ix_users_status'), table_name='users')
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_openid'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

    op.drop_index(op.f('ix_authors_dynasty'), table_name='authors')
    op.drop_index(op.f('ix_authors_name'), table_name='authors')
    op.drop_index(op.f('ix_authors_id'), table_name='authors')
    op.drop_table('authors')
