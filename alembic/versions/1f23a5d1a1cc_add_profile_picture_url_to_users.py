"""add profile_picture_url to users

Revision ID: 1f23a5d1a1cc
Revises: 25d814bc83ed
Create Date: 2025-05-02 19:18:19.976156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f23a5d1a1cc'
down_revision: Union[str, None] = '25d814bc83ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
