"""
Subscription Management API
Handles modules, packages, and pricing configuration.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.dependencies import get_current_super_admin
from app.models.user import User
from app.models.module import Module
from app.models.subscription_package import SubscriptionPackage
from app.models.package_module import PackageModule
from app.models.organization_module_addon import OrganizationModuleAddon
from app.models.organization import Organization
from app.schemas.subscription import (
    ModuleCreate, ModuleUpdate, ModuleResponse,
    SubscriptionPackageCreate, SubscriptionPackageUpdate, SubscriptionPackageResponse,
    SubscriptionPackagePublic, PackageModuleResponse,
    PricingTier, PricingResponse,
    ModuleAccessInfo, ModuleAccessResponse
)

router = APIRouter()


# ============ Module Endpoints ============

@router.get("/modules", response_model=List[ModuleResponse])
def get_all_modules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get all modules (Super Admin only)."""
    modules = db.query(Module).order_by(Module.display_order, Module.name).all()
    return modules


@router.post("/modules", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
def create_module(
    module_data: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Create a new module (Super Admin only)."""
    # Check if code already exists
    existing = db.query(Module).filter(Module.code == module_data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Module code already exists")

    module = Module(**module_data.model_dump())
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


@router.put("/modules/{module_id}", response_model=ModuleResponse)
def update_module(
    module_id: int,
    module_data: ModuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Update a module (Super Admin only)."""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    update_data = module_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(module, key, value)

    db.commit()
    db.refresh(module)
    return module


@router.delete("/modules/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Delete a module (Super Admin only)."""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Check if module is core - can't delete core modules
    if module.is_core:
        raise HTTPException(status_code=400, detail="Cannot delete core modules")

    db.delete(module)
    db.commit()
    return None


# ============ Subscription Package Endpoints ============

@router.get("/packages", response_model=List[SubscriptionPackageResponse])
def get_all_packages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get all subscription packages with included modules (Super Admin only)."""
    packages = db.query(SubscriptionPackage).order_by(
        SubscriptionPackage.display_order,
        SubscriptionPackage.monthly_price
    ).all()

    result = []
    for pkg in packages:
        pkg_dict = {
            "id": pkg.id,
            "name": pkg.name,
            "code": pkg.code,
            "description": pkg.description,
            "min_sites": pkg.min_sites,
            "max_sites": pkg.max_sites,
            "monthly_price": pkg.monthly_price,
            "annual_price": pkg.annual_price,
            "stripe_monthly_price_id": pkg.stripe_monthly_price_id,
            "stripe_annual_price_id": pkg.stripe_annual_price_id,
            "features_json": pkg.features_json,
            "is_active": pkg.is_active,
            "is_popular": pkg.is_popular,
            "display_order": pkg.display_order,
            "created_at": pkg.created_at,
            "updated_at": pkg.updated_at,
            "included_modules": []
        }

        # Get included modules
        for pm in pkg.package_modules:
            if pm.is_included:
                pkg_dict["included_modules"].append({
                    "module_id": pm.module.id,
                    "module_name": pm.module.name,
                    "module_code": pm.module.code,
                    "is_included": pm.is_included
                })

        result.append(pkg_dict)

    return result


@router.post("/packages", response_model=SubscriptionPackageResponse, status_code=status.HTTP_201_CREATED)
def create_package(
    package_data: SubscriptionPackageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Create a new subscription package (Super Admin only)."""
    # Check if code already exists
    existing = db.query(SubscriptionPackage).filter(
        SubscriptionPackage.code == package_data.code
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Package code already exists")

    # Create package
    pkg_dict = package_data.model_dump(exclude={"included_module_ids"})
    package = SubscriptionPackage(**pkg_dict)
    db.add(package)
    db.flush()  # Get the ID

    # Add included modules
    for module_id in package_data.included_module_ids:
        pm = PackageModule(package_id=package.id, module_id=module_id, is_included=True)
        db.add(pm)

    # Always add core modules
    core_modules = db.query(Module).filter(Module.is_core == True).all()
    existing_module_ids = set(package_data.included_module_ids)
    for core_module in core_modules:
        if core_module.id not in existing_module_ids:
            pm = PackageModule(package_id=package.id, module_id=core_module.id, is_included=True)
            db.add(pm)

    db.commit()
    db.refresh(package)

    # Return with modules
    return get_package_with_modules(package, db)


@router.put("/packages/{package_id}", response_model=SubscriptionPackageResponse)
def update_package(
    package_id: int,
    package_data: SubscriptionPackageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Update a subscription package (Super Admin only)."""
    package = db.query(SubscriptionPackage).filter(SubscriptionPackage.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    update_data = package_data.model_dump(exclude_unset=True, exclude={"included_module_ids"})
    for key, value in update_data.items():
        setattr(package, key, value)

    # Update included modules if provided
    if package_data.included_module_ids is not None:
        # Remove existing non-core module links
        db.query(PackageModule).filter(
            PackageModule.package_id == package_id
        ).delete()

        # Add new module links
        for module_id in package_data.included_module_ids:
            pm = PackageModule(package_id=package_id, module_id=module_id, is_included=True)
            db.add(pm)

        # Always add core modules
        core_modules = db.query(Module).filter(Module.is_core == True).all()
        existing_module_ids = set(package_data.included_module_ids)
        for core_module in core_modules:
            if core_module.id not in existing_module_ids:
                pm = PackageModule(package_id=package_id, module_id=core_module.id, is_included=True)
                db.add(pm)

    db.commit()
    db.refresh(package)

    return get_package_with_modules(package, db)


@router.delete("/packages/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Delete a subscription package (Super Admin only)."""
    package = db.query(SubscriptionPackage).filter(SubscriptionPackage.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    # Check if any organizations are using this package
    from app.models.organization import Organization
    orgs_using = db.query(Organization).filter(Organization.package_id == package_id).count()
    if orgs_using > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete package - {orgs_using} organization(s) are using it"
        )

    db.delete(package)
    db.commit()
    return None


# ============ Public Pricing Endpoint (for Landing Page) ============

@router.get("/pricing", response_model=PricingResponse)
def get_public_pricing(db: Session = Depends(get_db)):
    """Get public pricing information for landing page (no auth required)."""
    packages = db.query(SubscriptionPackage).filter(
        SubscriptionPackage.is_active == True
    ).order_by(
        SubscriptionPackage.display_order,
        SubscriptionPackage.monthly_price
    ).all()

    tiers = []
    for pkg in packages:
        # Build site range string
        if pkg.max_sites is None:
            site_range = f"{pkg.min_sites}+ sites"
        elif pkg.min_sites == pkg.max_sites:
            site_range = f"{pkg.min_sites} site" if pkg.min_sites == 1 else f"{pkg.min_sites} sites"
        else:
            site_range = f"{pkg.min_sites}-{pkg.max_sites} sites"

        # Parse features from JSON
        features = []
        if pkg.features_json:
            try:
                features = json.loads(pkg.features_json)
            except json.JSONDecodeError:
                features = []

        # Get included module names
        included_modules = []
        for pm in pkg.package_modules:
            if pm.is_included and pm.module:
                included_modules.append(pm.module.name)

        tiers.append(PricingTier(
            id=pkg.id,
            name=pkg.name,
            code=pkg.code,
            description=pkg.description,
            site_range=site_range,
            monthly_price=pkg.monthly_price,
            annual_price=pkg.annual_price,
            features=features,
            included_modules=included_modules,
            is_popular=pkg.is_popular
        ))

    # Get available add-on modules (non-core with pricing)
    addons = db.query(Module).filter(
        Module.is_active == True,
        Module.is_core == False,
        (Module.addon_price_per_site != None) | (Module.addon_price_per_org != None)
    ).order_by(Module.display_order, Module.name).all()

    return PricingResponse(tiers=tiers, available_addons=addons)


# ============ Helper Functions ============

def get_package_with_modules(package: SubscriptionPackage, db: Session) -> dict:
    """Get package data with included modules."""
    return {
        "id": package.id,
        "name": package.name,
        "code": package.code,
        "description": package.description,
        "min_sites": package.min_sites,
        "max_sites": package.max_sites,
        "monthly_price": package.monthly_price,
        "annual_price": package.annual_price,
        "stripe_monthly_price_id": package.stripe_monthly_price_id,
        "stripe_annual_price_id": package.stripe_annual_price_id,
        "features_json": package.features_json,
        "is_active": package.is_active,
        "is_popular": package.is_popular,
        "display_order": package.display_order,
        "created_at": package.created_at,
        "updated_at": package.updated_at,
        "included_modules": [
            {
                "module_id": pm.module.id,
                "module_name": pm.module.name,
                "module_code": pm.module.code,
                "is_included": pm.is_included
            }
            for pm in package.package_modules if pm.is_included
        ]
    }


# ============ Module Access Endpoints ============

@router.get("/my-access", response_model=ModuleAccessResponse)
def get_my_module_access(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get module access information for the current user's organization."""
    if not current_user.organization_id:
        raise HTTPException(status_code=400, detail="User has no organization")
    
    org = db.query(Organization).filter(Organization.id == current_user.organization_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Get all active modules
    all_modules = db.query(Module).filter(Module.is_active == True).order_by(Module.display_order, Module.name).all()
    
    # Get modules included in the org's package
    package_module_codes = set()
    if org.package_id:
        package_modules = db.query(PackageModule).filter(
            PackageModule.package_id == org.package_id,
            PackageModule.is_included == True
        ).all()
        for pm in package_modules:
            module = db.query(Module).filter(Module.id == pm.module_id).first()
            if module:
                package_module_codes.add(module.code)
    
    # Get addon modules purchased by the org
    addon_module_codes = set()
    org_addons = db.query(OrganizationModuleAddon).filter(
        OrganizationModuleAddon.organization_id == org.id,
        OrganizationModuleAddon.is_active == True
    ).all()
    for addon in org_addons:
        module = db.query(Module).filter(Module.id == addon.module_id).first()
        if module:
            addon_module_codes.add(module.code)
    
    # Build module access list
    modules_access = []
    for module in all_modules:
        has_access = False
        access_type = None
        
        if module.is_core:
            has_access = True
            access_type = "core"
        elif module.code in package_module_codes:
            has_access = True
            access_type = "package"
        elif module.code in addon_module_codes:
            has_access = True
            access_type = "addon"
        
        modules_access.append(ModuleAccessInfo(
            code=module.code,
            name=module.name,
            description=module.description,
            icon=module.icon,
            has_access=has_access,
            access_type=access_type,
            addon_price_per_site=module.addon_price_per_site,
            addon_price_per_org=module.addon_price_per_org
        ))
    
    return ModuleAccessResponse(
        organization_id=org.id,
        organization_name=org.name,
        package_code=org.subscription_package.code if org.subscription_package else None,
        package_name=org.subscription_package.name if org.subscription_package else None,
        is_trial=org.is_trial,
        modules=modules_access
    )


@router.get("/check-access/{module_code}")
def check_module_access(
    module_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if the current user's organization has access to a specific module."""
    if not current_user.organization_id:
        return {"has_access": False, "reason": "no_organization"}
    
    org = db.query(Organization).filter(Organization.id == current_user.organization_id).first()
    if not org:
        return {"has_access": False, "reason": "organization_not_found"}
    
    # Check if module exists
    module = db.query(Module).filter(Module.code == module_code, Module.is_active == True).first()
    if not module:
        return {"has_access": False, "reason": "module_not_found"}
    
    # Core modules are always accessible
    if module.is_core:
        return {"has_access": True, "access_type": "core"}
    
    # Check if module is included in org's package
    if org.package_id:
        package_module = db.query(PackageModule).filter(
            PackageModule.package_id == org.package_id,
            PackageModule.module_id == module.id,
            PackageModule.is_included == True
        ).first()
        if package_module:
            return {"has_access": True, "access_type": "package"}
    
    # Check if org has purchased this module as an addon
    addon = db.query(OrganizationModuleAddon).filter(
        OrganizationModuleAddon.organization_id == org.id,
        OrganizationModuleAddon.module_id == module.id,
        OrganizationModuleAddon.is_active == True
    ).first()
    if addon:
        return {"has_access": True, "access_type": "addon"}
    
    # No access - return upgrade info
    return {
        "has_access": False,
        "reason": "not_in_package",
        "module_name": module.name,
        "addon_price_per_site": module.addon_price_per_site,
        "addon_price_per_org": module.addon_price_per_org
    }
