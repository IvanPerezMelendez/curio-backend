"""users_jwt_auth

Revision ID: z_20260523200000
Revises: z_20260523185605
Create Date: 2026-05-23 20:00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'z_20260523200000'
down_revision: Union[str, None] = 'z_20260523185605'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'anonymous_id')
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('hashed_password', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))
    op.create_unique_constraint(op.f('uq_users_email'), 'users', ['email'])


def downgrade() -> None:
    op.drop_constraint(op.f('uq_users_email'), 'users', type_='unique')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'email')
    op.add_column('users', sa.Column(
        'anonymous_id',
        sa.UUID(),
        nullable=False,
    ))
    op.create_unique_constraint(op.f('uq_users_anonymous_id'), 'users', ['anonymous_id'])
