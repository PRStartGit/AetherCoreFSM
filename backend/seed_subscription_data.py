"""
Seed script to populate subscription packages and modules.
Run this once to set up initial pricing configuration.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.module import Module
from app.models.subscription_package import SubscriptionPackage
from app.models.package_module import PackageModule
import json


def seed_modules(db: Session):
    """Create default modules."""
    modules_data = [
        {
            "name": "Checklists & Monitoring",
            "code": "checklists",
            "description": "Daily checklists, temperature monitoring, and compliance tracking",
            "icon": "clipboard-check",
            "is_core": True,
            "display_order": 1
        },
        {
            "name": "Defect Management",
            "code": "defects",
            "description": "Track and resolve defects with photo evidence and assignments",
            "icon": "alert-triangle",
            "is_core": True,
            "display_order": 2
        },
        {
            "name": "Zynthio Recipes",
            "code": "recipes",
            "description": "Recipe management with allergen tracking and costing",
            "icon": "book-open",
            "is_core": False,
            "addon_price_per_site": 2.00,
            "display_order": 3
        },
        {
            "name": "Zynthio Training",
            "code": "training",
            "description": "Staff training modules with progress tracking and certifications",
            "icon": "graduation-cap",
            "is_core": False,
            "addon_price_per_org": 5.00,
            "display_order": 4
        }
    ]

    created_modules = {}
    for data in modules_data:
        existing = db.query(Module).filter(Module.code == data["code"]).first()
        if existing:
            print(f"Module '{data['code']}' already exists, skipping...")
            created_modules[data["code"]] = existing
        else:
            module = Module(**data)
            db.add(module)
            db.flush()
            created_modules[data["code"]] = module
            print(f"Created module: {data['name']}")

    return created_modules


def seed_packages(db: Session, modules: dict):
    """Create default subscription packages."""
    packages_data = [
        {
            "name": "Free",
            "code": "free",
            "description": "Perfect for trying out Zynthio",
            "min_sites": 1,
            "max_sites": 1,
            "monthly_price": 0.00,
            "annual_price": 0.00,
            "features_json": json.dumps([
                "1 site included",
                "Core checklists & monitoring",
                "Defect tracking",
                "Basic reporting",
                "Email support"
            ]),
            "is_active": True,
            "is_popular": False,
            "display_order": 1,
            "modules": ["checklists", "defects"]
        },
        {
            "name": "Starter",
            "code": "starter",
            "description": "Great for small businesses",
            "min_sites": 2,
            "max_sites": 3,
            "monthly_price": 29.00,
            "annual_price": 290.00,
            "features_json": json.dumps([
                "Up to 3 sites",
                "All core modules",
                "Advanced reporting",
                "Priority email support",
                "Data export"
            ]),
            "is_active": True,
            "is_popular": False,
            "display_order": 2,
            "modules": ["checklists", "defects"]
        },
        {
            "name": "Professional",
            "code": "professional",
            "description": "For growing businesses",
            "min_sites": 4,
            "max_sites": 10,
            "monthly_price": 79.00,
            "annual_price": 790.00,
            "features_json": json.dumps([
                "Up to 10 sites",
                "All modules included",
                "Custom checklists",
                "Advanced analytics",
                "Phone support",
                "API access"
            ]),
            "is_active": True,
            "is_popular": True,
            "display_order": 3,
            "modules": ["checklists", "defects", "recipes", "training"]
        },
        {
            "name": "Enterprise",
            "code": "enterprise",
            "description": "For large organizations",
            "min_sites": 11,
            "max_sites": None,
            "monthly_price": 149.00,
            "annual_price": 1490.00,
            "features_json": json.dumps([
                "Unlimited sites",
                "All modules included",
                "Custom integrations",
                "Dedicated account manager",
                "24/7 priority support",
                "On-site training",
                "SLA guarantee"
            ]),
            "is_active": True,
            "is_popular": False,
            "display_order": 4,
            "modules": ["checklists", "defects", "recipes", "training"]
        }
    ]

    for data in packages_data:
        existing = db.query(SubscriptionPackage).filter(
            SubscriptionPackage.code == data["code"]
        ).first()

        if existing:
            print(f"Package '{data['code']}' already exists, skipping...")
            continue

        module_codes = data.pop("modules")
        package = SubscriptionPackage(**data)
        db.add(package)
        db.flush()

        # Link modules to package
        for code in module_codes:
            if code in modules:
                pm = PackageModule(
                    package_id=package.id,
                    module_id=modules[code].id,
                    is_included=True
                )
                db.add(pm)

        print(f"Created package: {data['name']} (£{data['monthly_price']}/mo)")


def main():
    """Main seed function."""
    print("=" * 50)
    print("Seeding Subscription Data")
    print("=" * 50)

    db = SessionLocal()
    try:
        # Seed modules first
        print("\n--- Creating Modules ---")
        modules = seed_modules(db)

        # Seed packages
        print("\n--- Creating Packages ---")
        seed_packages(db, modules)

        # Commit all changes
        db.commit()
        print("\n" + "=" * 50)
        print("Subscription data seeded successfully!")
        print("=" * 50)

    except Exception as e:
        db.rollback()
        print(f"\nError seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
