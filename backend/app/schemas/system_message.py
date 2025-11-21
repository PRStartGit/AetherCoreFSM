from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class VisibilityScopeEnum(str, Enum):
    ORG_ADMINS_ONLY = "org_admins_only"
    SITE_USERS_ONLY = "site_users_only"
    BOTH = "both"
    ORGANIZATION = "organization"


class SystemMessageCreate(BaseModel):
    message_content: str
    expiry_date: datetime
    visibility_scope: VisibilityScopeEnum = VisibilityScopeEnum.BOTH


class SystemMessageResponse(BaseModel):
    id: int
    message_content: str
    created_by_user_id: int
    created_by_name: Optional[str] = None
    organization_id: Optional[int] = None
    organization_name: Optional[str] = None
    visibility_scope: str
    expiry_date: datetime
    is_active: bool
    created_at: datetime
    is_super_admin_message: bool = False

    class Config:
        from_attributes = True


class SystemMessageList(BaseModel):
    messages: list[SystemMessageResponse]
    total: int


class MessageDismissRequest(BaseModel):
    message_id: int
