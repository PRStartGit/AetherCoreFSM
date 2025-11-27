from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ============ Module Schemas ============

class ModuleBase(BaseModel):
    """Base module schema."""
    name: str
    code: str
    description: Optional[str] = None
    icon: Optional[str] = None
    is_core: bool = False
    addon_price_per_site: Optional[float] = None
    addon_price_per_org: Optional[float] = None
    is_active: bool = True
    display_order: int = 0


class ModuleCreate(ModuleBase):
    """Module creation schema."""
    pass


class ModuleUpdate(BaseModel):
    """Module update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    is_core: Optional[bool] = None
    addon_price_per_site: Optional[float] = None
    addon_price_per_org: Optional[float] = None
    gocardless_addon_plan_id: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class ModuleResponse(ModuleBase):
    """Module response schema."""
    id: int
    gocardless_addon_plan_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============ Subscription Package Schemas ============

class SubscriptionPackageBase(BaseModel):
    """Base subscription package schema."""
    name: str
    code: str
    description: Optional[str] = None
    min_sites: int = 1
    max_sites: Optional[int] = None
    monthly_price: float = 0.0
    annual_price: Optional[float] = None
    features_json: Optional[str] = None
    is_active: bool = True
    is_popular: bool = False
    display_order: int = 0


class SubscriptionPackageCreate(SubscriptionPackageBase):
    """Subscription package creation schema."""
    included_module_ids: List[int] = []


class SubscriptionPackageUpdate(BaseModel):
    """Subscription package update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    min_sites: Optional[int] = None
    max_sites: Optional[int] = None
    monthly_price: Optional[float] = None
    annual_price: Optional[float] = None
    gocardless_plan_id: Optional[str] = None
    gocardless_annual_plan_id: Optional[str] = None
    features_json: Optional[str] = None
    is_active: Optional[bool] = None
    is_popular: Optional[bool] = None
    display_order: Optional[int] = None
    included_module_ids: Optional[List[int]] = None


class PackageModuleResponse(BaseModel):
    """Package module relationship response."""
    module_id: int
    module_name: str
    module_code: str
    is_included: bool

    class Config:
        from_attributes = True


class SubscriptionPackageResponse(SubscriptionPackageBase):
    """Subscription package response schema."""
    id: int
    gocardless_plan_id: Optional[str] = None
    gocardless_annual_plan_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    included_modules: List[PackageModuleResponse] = []

    class Config:
        from_attributes = True


class SubscriptionPackagePublic(BaseModel):
    """Public subscription package for landing page (no Stripe IDs)."""
    id: int
    name: str
    code: str
    description: Optional[str] = None
    min_sites: int
    max_sites: Optional[int] = None
    monthly_price: float
    annual_price: Optional[float] = None
    features: List[str] = []
    is_popular: bool = False
    included_modules: List[str] = []  # Module names only

    class Config:
        from_attributes = True


# ============ Organization Module Addon Schemas ============

class OrganizationModuleAddonBase(BaseModel):
    """Base organization module addon schema."""
    module_id: int
    is_active: bool = True


class OrganizationModuleAddonCreate(OrganizationModuleAddonBase):
    """Organization module addon creation schema."""
    organization_id: int


class OrganizationModuleAddonResponse(OrganizationModuleAddonBase):
    """Organization module addon response schema."""
    id: int
    organization_id: int
    module_name: Optional[str] = None
    stripe_subscription_item_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============ Pricing Display Schema (for Landing Page) ============

class PricingTier(BaseModel):
    """Pricing tier for landing page display."""
    id: int
    name: str
    code: str
    description: Optional[str] = None
    site_range: str  # e.g., "1 site", "2-3 sites", "4-10 sites", "11+ sites"
    monthly_price: float
    annual_price: Optional[float] = None
    features: List[str] = []
    included_modules: List[str] = []
    is_popular: bool = False


class PricingResponse(BaseModel):
    """Full pricing response for landing page."""
    tiers: List[PricingTier] = []
    available_addons: List[ModuleResponse] = []


# ============ Module Access Control Schemas ============

class ModuleAccessInfo(BaseModel):
    """Information about a module and access status."""
    code: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    has_access: bool
    access_type: Optional[str] = None  # "core", "package", "addon", None
    addon_price_per_site: Optional[float] = None
    addon_price_per_org: Optional[float] = None


class ModuleAccessResponse(BaseModel):
    """Response containing all module access information for an organization."""
    organization_id: int
    organization_name: str
    package_code: Optional[str] = None
    package_name: Optional[str] = None
    is_trial: bool = False
    modules: List[ModuleAccessInfo] = []


class UpgradeOption(BaseModel):
    """Upgrade option for module access."""
    type: str  # "package_upgrade" or "addon_purchase"
    package_code: Optional[str] = None
    package_name: Optional[str] = None
    monthly_price: Optional[float] = None
    addon_price_per_site: Optional[float] = None
    addon_price_per_org: Optional[float] = None
