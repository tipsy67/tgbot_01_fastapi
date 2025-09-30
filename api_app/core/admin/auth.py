from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form["username"]
        password = form["password"]

        # Validate username/password credentials
        # And update session
        request.session.update({"token": "token!"})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        if token == "token!":
            return True

        return False

