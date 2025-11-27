"""Add subscription and module tables

Revision ID: 2025_11_27_1700
Revises: 2025_11_26_2000
Create Date: 2025-11-27 17:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

revision = '2025_11_27_1700'
down_revision = '2025_11_26_2000'
branch_labels = None
depends_on = None


def upgrade():
    # Create modules table
    op.create_table(
        'modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(), nullable=True),
        sa.Column('is_core', sa.Boolean(), default=False),
        sa.Column('addon_price_per_site', sa.Float(), nullable=True),
        sa.Column('addon_price_per_org', sa.Float(), nullable=True),
        sa.Column('gocardless_addon_plan_id', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('display_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_modules_code', 'modules', ['code'], unique=True)

    # Create subscription_packages table
    op.create_table(
        'subscription_packages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('min_sites', sa.Integer(), nullable=False, default=1),
        sa.Column('max_sites', sa.Integer(), nullable=True),
        sa.Column('monthly_price', sa.Float(), nullable=False, default=0.0),
        sa.Column('annual_price', sa.Float(), nullable=True),
        sa.Column('gocardless_plan_id', sa.String(), nullable=True),
        sa.Column('gocardless_annual_plan_id', sa.String(), nullable=True),
        sa.Column('features_json', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_popular', sa.Boolean(), default=False),
        sa.Column('display_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_subscription_packages_code', 'subscription_packages', ['code'], unique=True)

    # Create package_modules junction table
    op.create_table(
        'package_modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('package_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('is_included', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['package_id'], ['subscription_packages.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_package_modules_package', 'package_modules', ['package_id'])
    op.create_index('ix_package_modules_module', 'package_modules', ['module_id'])

    # Create organization_module_addons table
    op.create_table(
        'organization_module_addons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('price_override', sa.Float(), nullable=True),
        sa.Column('gocardless_subscription_id', sa.String(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('cancelled_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_org_module_addons_org', 'organization_module_addons', ['organization_id'])

    # Add columns to organizations table (without foreign key for SQLite compatibility)
    op.add_column('organizations', sa.Column('gocardless_customer_id', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('gocardless_mandate_id', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('gocardless_subscription_id', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('package_id', sa.Integer(), nullable=True))
    op.create_index('ix_organizations_gocardless_customer', 'organizations', ['gocardless_customer_id'])
    
    # Only add foreign key for non-SQLite
    bind = op.get_bind()
    if bind.dialect.name != 'sqlite':
        op.create_foreign_key('fk_organizations_package', 'organizations', 'subscription_packages', ['package_id'], ['id'])


def downgrade():
    bind = op.get_bind()
    if bind.dialect.name != 'sqlite':
        op.drop_constraint('fk_organizations_package', 'organizations', type_='foreignkey')
    
    op.drop_index('ix_organizations_gocardless_customer', table_name='organizations')
    op.drop_column('organizations', 'package_id')
    op.drop_column('organizations', 'gocardless_subscription_id')
    op.drop_column('organizations', 'gocardless_mandate_id')
    op.drop_column('organizations', 'gocardless_customer_id')

    op.drop_index('ix_org_module_addons_org', table_name='organization_module_addons')
    op.drop_table('organization_module_addons')

    op.drop_index('ix_package_modules_module', table_name='package_modules')
    op.drop_index('ix_package_modules_package', table_name='package_modules')
    op.drop_table('package_modules')

    op.drop_index('ix_subscription_packages_code', table_name='subscription_packages')
    op.drop_table('subscription_packages')

    op.drop_index('ix_modules_code', table_name='modules')
    op.drop_table('modules')
