"""
Database seeding script
Creates initial data for testing:
- Super admin user
- Test organizations
- Test sites
- Test users
"""
import sys
from datetime import datetime, timedelta

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.site import Site
from app.models.organization_module import OrganizationModule


def seed_database():
    """Seed the database with initial data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if super admin already exists
        existing_admin = db.query(User).filter(
            User.role == UserRole.SUPER_ADMIN
        ).first()

        if existing_admin:
            print("Database already seeded. Skipping...")
            return

        print("\n🌱 Seeding database...")

        # 1. Create Super Admin
        print("\n1️⃣  Creating Super Admin...")
        super_admin = User(
            email="admin@riskproof.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Super",
            last_name="Admin",
            role=UserRole.SUPER_ADMIN,
            phone="+44 20 1234 5678",
            is_active=True
        )
        db.add(super_admin)
        db.flush()
        print(f"   ✅ Super Admin created: {super_admin.email} / admin123")

        # 2. Create Organizations
        print("\n2️⃣  Creating Organizations...")

        # Organization 1: Viva Italia Group
        org1 = Organization(
            name="Viva Italia Group",
            org_id="vig",
            contact_person="Mario Rossi",
            contact_email="mario@vivaitaliagroup.com",
            contact_phone="+44 20 7123 4567",
            address="123 Italian Street, London, UK",
            subscription_tier="professional",
            is_trial=True,
            subscription_start_date=datetime.utcnow(),
            subscription_end_date=datetime.utcnow() + timedelta(days=365)
        )
        db.add(org1)
        db.flush()
        print(f"   ✅ {org1.name} (org_id: {org1.org_id})")

        # Organization 2: Best Restaurants Ltd
        org2 = Organization(
            name="Best Restaurants Ltd",
            org_id="brl",
            contact_person="John Smith",
            contact_email="john@bestrestaurants.co.uk",
            contact_phone="+44 20 8765 4321",
            address="456 Food Avenue, Manchester, UK",
            subscription_tier="basic",
            is_trial=True,
            subscription_start_date=datetime.utcnow(),
            subscription_end_date=datetime.utcnow() + timedelta(days=365)
        )
        db.add(org2)
        db.flush()
        print(f"   ✅ {org2.name} (org_id: {org2.org_id})")

        # Organization 3: Safe Food Chain
        org3 = Organization(
            name="Safe Food Chain",
            org_id="sfc",
            contact_person="Sarah Johnson",
            contact_email="sarah@safefoodchain.com",
            contact_phone="+44 20 5555 1234",
            address="789 Safety Road, Birmingham, UK",
            subscription_tier="enterprise",
            is_trial=False,
            custom_price_per_site=45.00,
            subscription_start_date=datetime.utcnow(),
            subscription_end_date=datetime.utcnow() + timedelta(days=365)
        )
        db.add(org3)
        db.flush()
        print(f"   ✅ {org3.name} (org_id: {org3.org_id})")

        # 3. Enable Modules for Organizations
        print("\n3️⃣  Enabling Modules...")
        modules = ["monitoring", "audit", "training", "policy", "documents"]

        for org in [org1, org2, org3]:
            for module in modules:
                org_module = OrganizationModule(
                    organization_id=org.id,
                    module_name=module,
                    is_enabled=True
                )
                db.add(org_module)
        db.flush()
        print("   ✅ Modules enabled for all organizations")

        # 4. Create Sites
        print("\n4️⃣  Creating Sites...")

        # Sites for Viva Italia Group
        vig_sites = [
            {"name": "Bella Italia Soho", "site_code": "VIG-001", "city": "London"},
            {"name": "Bella Italia Covent Garden", "site_code": "VIG-002", "city": "London"},
            {"name": "Bella Italia Oxford Street", "site_code": "VIG-003", "city": "London"},
            {"name": "Bella Italia Manchester", "site_code": "VIG-004", "city": "Manchester"},
            {"name": "Bella Italia Birmingham", "site_code": "VIG-005", "city": "Birmingham"},
        ]

        for site_data in vig_sites:
            site = Site(
                organization_id=org1.id,
                name=site_data["name"],
                site_code=site_data["site_code"],
                city=site_data["city"],
                country="UK",
                is_active=True,
                daily_report_enabled=True,
                daily_report_time="09:00"
            )
            db.add(site)
            print(f"   ✅ {site.name}")

        # Sites for Best Restaurants Ltd
        brl_sites = [
            {"name": "Best Burger King Street", "site_code": "BRL-001", "city": "Manchester"},
            {"name": "Best Burger Deansgate", "site_code": "BRL-002", "city": "Manchester"},
            {"name": "Best Burger Trafford", "site_code": "BRL-003", "city": "Manchester"},
        ]

        for site_data in brl_sites:
            site = Site(
                organization_id=org2.id,
                name=site_data["name"],
                site_code=site_data["site_code"],
                city=site_data["city"],
                country="UK",
                is_active=True
            )
            db.add(site)
            print(f"   ✅ {site.name}")

        # Sites for Safe Food Chain
        sfc_sites = [
            {"name": "Safe Food Birmingham Central", "site_code": "SFC-001", "city": "Birmingham"},
            {"name": "Safe Food Birmingham North", "site_code": "SFC-002", "city": "Birmingham"},
        ]

        for site_data in sfc_sites:
            site = Site(
                organization_id=org3.id,
                name=site_data["name"],
                site_code=site_data["site_code"],
                city=site_data["city"],
                country="UK",
                is_active=True
            )
            db.add(site)
            print(f"   ✅ {site.name}")

        db.flush()

        # 5. Create Users
        print("\n5️⃣  Creating Users...")

        # Org Admin for VIG
        vig_admin = User(
            email="admin@vivaitaliagroup.com",
            hashed_password=get_password_hash("password123"),
            first_name="Luigi",
            last_name="Romano",
            role=UserRole.ORG_ADMIN,
            organization_id=org1.id,
            phone="+44 20 7123 4567",
            is_active=True
        )
        db.add(vig_admin)
        print(f"   ✅ Org Admin: {vig_admin.email} / password123")

        # Site User for VIG
        vig_user = User(
            email="manager@vivaitaliagroup.com",
            hashed_password=get_password_hash("password123"),
            first_name="Marco",
            last_name="Bianchi",
            role=UserRole.SITE_USER,
            organization_id=org1.id,
            phone="+44 20 7123 4568",
            is_active=True
        )
        db.add(vig_user)
        print(f"   ✅ Site User: {vig_user.email} / password123")

        # Org Admin for BRL
        brl_admin = User(
            email="admin@bestrestaurants.co.uk",
            hashed_password=get_password_hash("password123"),
            first_name="David",
            last_name="Brown",
            role=UserRole.ORG_ADMIN,
            organization_id=org2.id,
            phone="+44 20 8765 4321",
            is_active=True
        )
        db.add(brl_admin)
        print(f"   ✅ Org Admin: {brl_admin.email} / password123")

        # Org Admin for SFC
        sfc_admin = User(
            email="admin@safefoodchain.com",
            hashed_password=get_password_hash("password123"),
            first_name="Emma",
            last_name="Wilson",
            role=UserRole.ORG_ADMIN,
            organization_id=org3.id,
            phone="+44 20 5555 1234",
            is_active=True
        )
        db.add(sfc_admin)
        print(f"   ✅ Org Admin: {sfc_admin.email} / password123")

        # Commit all changes
        db.commit()

        print("\n✨ Database seeding completed successfully!")
        print("\n📝 Summary:")
        print(f"   - 1 Super Admin")
        print(f"   - 3 Organizations (vig, brl, sfc)")
        print(f"   - 10 Sites total")
        print(f"   - 5 Users (1 super admin + 4 org users)")
        print("\n🔑 Login Credentials:")
        print("   Super Admin: admin@riskproof.com / admin123")
        print("   VIG Admin: admin@vivaitaliagroup.com / password123")
        print("   BRL Admin: admin@bestrestaurants.co.uk / password123")
        print("   SFC Admin: admin@safefoodchain.com / password123")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
