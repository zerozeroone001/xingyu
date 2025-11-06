"""添加关注表

Revision ID: 004
Revises: 003
Create Date: 2025-11-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建follows表
    op.create_table(
        'follows',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='ID'),
        sa.Column('user_id', sa.BigInteger(), nullable=False, comment='关注者ID'),
        sa.Column('follow_user_id', sa.BigInteger(), nullable=False, comment='被关注者ID'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间'),
        sa.ForeignKeyConstraint(['follow_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'follow_user_id', name='uk_user_follow'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_engine='InnoDB',
        comment='关注表'
    )
    op.create_index(op.f('ix_follows_id'), 'follows', ['id'], unique=False)
    op.create_index(op.f('ix_follows_user_id'), 'follows', ['user_id'], unique=False)
    op.create_index(op.f('ix_follow_user_id'), 'follows', ['follow_user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_follow_user_id'), table_name='follows')
    op.drop_index(op.f('ix_follows_user_id'), table_name='follows')
    op.drop_index(op.f('ix_follows_id'), table_name='follows')
    op.drop_table('follows')
