"""
Migration script to set all existing organizations to 12-month trial.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.organization import Organization
from app.models.subscription_package import SubscriptionPackage


def migrate_orgs_to_trial():
    """Set all existing organizations to 12-month trial period."""
    db = SessionLocal()

    try:
        # Get the Professional package as the default trial package
        professional_package = db.query(SubscriptionPackage).filter(
            SubscriptionPackage.code == "professional"
        ).first()

        if not professional_package:
            print("Warning: Professional package not found. Will set trial without package.")
            package_id = None
        else:
            package_id = professional_package.id
            print(f"Using Professional package (ID: {package_id}) for trial")

        # Get all organizations
        orgs = db.query(Organization).all()

        now = datetime.utcnow()
        trial_end = now + timedelta(days=365)  # 12 months

        updated_count = 0
        for org in orgs:
            # Skip platform admin org if exists
            if org.subscription_tier == "platform_admin":
                print(f"Skipping platform admin org: {org.name}")
                continue

            org.is_trial = True
            org.subscription_start_date = now
            org.subscription_end_date = trial_end

            # Set package if not already set
            if not org.package_id and package_id:
                org.package_id = package_id

            updated_count += 1
            print(f"Updated: {org.name} ({org.org_id}) - Trial until {trial_end.strftime('%Y-%m-%d')}")

        db.commit()
        print(f"\nMigration complete! Updated {updated_count} organizations to 12-month trial.")
        print(f"Trial end date: {trial_end.strftime('%Y-%m-%d')}")

    except Exception as e:
        db.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Organization Trial Migration")
    print("=" * 60)
    migrate_orgs_to_trial()
