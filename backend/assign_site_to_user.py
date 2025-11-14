"""Assign site to site user."""
from app.core.database import SessionLocal
from app.models.user import User
from app.models.site import Site
from app.models.user_site import UserSite

db = SessionLocal()

try:
    # Get site user
    user = db.query(User).filter(User.email == 'siteuser@vivaitaliagroup.com').first()
    if not user:
        print("[ERROR] Site user not found!")
        exit(1)

    # Get site
    site = db.query(Site).filter(Site.site_code == "VIG-001").first()
    if not site:
        print("[ERROR] Site VIG-001 not found!")
        exit(1)

    # Check if already assigned
    existing = db.query(UserSite).filter(
        UserSite.user_id == user.id,
        UserSite.site_id == site.id
    ).first()

    if existing:
        print(f"[SKIP] User already assigned to site {site.name}")
    else:
        # Create assignment
        user_site = UserSite(
            user_id=user.id,
            site_id=site.id
        )
        db.add(user_site)
        db.commit()
        print(f"[OK] Assigned {user.email} to site {site.name} ({site.site_code})")

finally:
    db.close()
