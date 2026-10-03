from app.schemas.auth import LoginRequest, Token
from app.core.security import create_access_token


class AuthService:
    async def login(self, req: LoginRequest) -> Token:
        # Mock auth token for bootstrapping phase
        token = create_access_token(subject=req.email)
        return Token(access_token=token, user_id="user-demo-admin", role="admin")


auth_service = AuthService()
