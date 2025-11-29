"""Add blog posts table

Revision ID: add_blog_posts_table
Revises: add_reporting_module
Create Date: 2025-11-29 15:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_blog_posts_table'
down_revision = 'add_reporting_module'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'blog_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('excerpt', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('thumbnail_url', sa.String(500), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=False, default=False),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_blog_posts_id', 'blog_posts', ['id'])
    op.create_index('ix_blog_posts_slug', 'blog_posts', ['slug'], unique=True)


def downgrade():
    op.drop_index('ix_blog_posts_slug', table_name='blog_posts')
    op.drop_index('ix_blog_posts_id', table_name='blog_posts')
    op.drop_table('blog_posts')
