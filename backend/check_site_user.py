"""Check site user assignments and checklists."""
from app.core.database import SessionLocal
from app.models.user import User
from app.models.site import Site
from app.models.user_site import UserSite
from app.models.checklist import Checklist
from datetime import date

db = SessionLocal()

try:
    # Get site user
    user = db.query(User).filter(User.email == 'siteuser@vivaitaliagroup.com').first()
    if not user:
        print("[ERROR] Site user not found!")
        exit(1)

    print(f"\n=== SITE USER INFO ===")
    print(f"User ID: {user.id}")
    print(f"Name: {user.first_name} {user.last_name}")
    print(f"Email: {user.email}")
    print(f"Role: {user.role}")
    print(f"Organization ID: {user.organization_id}")

    # Check assigned sites
    print(f"\n=== ASSIGNED SITES ===")
    user_sites = db.query(UserSite).filter(UserSite.user_id == user.id).all()
    print(f"Number of assigned sites: {len(user_sites)}")

    if user_sites:
        for us in user_sites:
            site = db.query(Site).filter(Site.id == us.site_id).first()
            print(f"  - Site: {site.name} (ID: {site.id}, Code: {site.site_code})")
    else:
        print("  [WARNING] No sites assigned to this user!")

    # Check checklists for today
    today = date.today()
    print(f"\n=== CHECKLISTS FOR TODAY ({today}) ===")

    if user_sites:
        for us in user_sites:
            site = db.query(Site).filter(Site.id == us.site_id).first()
            checklists = db.query(Checklist).filter(
                Checklist.site_id == site.id,
                Checklist.checklist_date == today
            ).all()

            print(f"\nSite: {site.name} (ID: {site.id})")
            print(f"  Checklists: {len(checklists)}")
            for checklist in checklists:
                print(f"    - Category ID: {checklist.category_id}, Status: {checklist.status}, Items: {checklist.completed_items}/{checklist.total_items}")

    # Check all checklists for the site
    print(f"\n=== ALL CHECKLISTS FOR VIG-001 ===")
    site = db.query(Site).filter(Site.site_code == "VIG-001").first()
    if site:
        all_checklists = db.query(Checklist).filter(Checklist.site_id == site.id).all()
        print(f"Total checklists: {len(all_checklists)}")
        for checklist in all_checklists:
            print(f"  - Date: {checklist.checklist_date}, Category: {checklist.category_id}, Status: {checklist.status}")

finally:
    db.close()
