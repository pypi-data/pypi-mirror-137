from datetime import datetime
from typing import List, Optional

from pydantic import AnyUrl, EmailStr, Field

from fa_common.models import CamelModel


class AuthUser(CamelModel):
    sub: str
    name: str = "Unknown User"
    email: Optional[EmailStr]
    nickname: Optional[str] = None
    email_verified: bool = Field(False, title="Email Verified")
    picture: Optional[AnyUrl] = None
    updated_at: Optional[datetime] = Field(None, title="Updated At")
    scopes: List[str] = []
    roles: List[str] = []
