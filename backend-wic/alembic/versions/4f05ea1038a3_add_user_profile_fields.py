"""add user profile fields

Revision ID: 4f05ea1038a3
Revises: ffee422ddc98
Create Date: 2026-06-09 00:30:07.928433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4f05ea1038a3'
down_revision: Union[str, Sequence[str], None] = 'ffee422ddc98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('student_id', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('real_name', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('department', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('major', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('class_name', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('grade', sa.String(length=10), nullable=True))
    op.create_index(op.f('ix_users_student_id'), 'users', ['student_id'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_student_id'), table_name='users')
    op.drop_column('users', 'grade')
    op.drop_column('users', 'class_name')
    op.drop_column('users', 'major')
    op.drop_column('users', 'department')
    op.drop_column('users', 'real_name')
    op.drop_column('users', 'student_id')
