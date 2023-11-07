from datetime import datetime, timezone
import os

from dateutil.relativedelta import relativedelta
from fastapi import Header, HTTPException, APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/authenticate')

password = os.getenv("ADMIN_PASSWORD", "password")
authenticated_cookie = os.getenv("AUTH_COOKIE_VALUE", "0000-0000-0000-0000")


def is_authenticated(request: Request):
    return request.cookies.get("auth_key") == authenticated_cookie


@router.post("/")
async def authenticate(request: Request):
    if is_authenticated(request):
        return JSONResponse(content={"authenticated": True})

    admin_password = request.headers.get("admin_password")
    if admin_password != password:
        raise HTTPException(status_code=404)

    response = JSONResponse(content={"authenticated": True})
    response.set_cookie(key="auth_key", value=authenticated_cookie, httponly=True, secure=True, samesite="Lax", max_age=60 * 60 * 24 * 365, expires=datetime.now(timezone.utc) + relativedelta(years=1))
    return response
