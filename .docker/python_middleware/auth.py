import time
import httpx
import jwt
import yaml
from jwt import PyJWKClient
from functools import lru_cache
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException
from pydantic_settings import BaseSettings

# ======================
# CONFIG
# ======================

class Settings(BaseSettings):
    # دو تا URL جدا برای issuer و تماس‌های داخلی
    KEYCLOAK_PUBLIC_URL: str
    KEYCLOAK_INTERNAL_URL: str
    REALM: str
    CLIENT_ID: str | None = None
    CLIENT_SECRET: str | None = None
    JWKS_CACHE_TTL: int = 3600
    CONFIG_FILE: str = "projects.yml"
    CONFIG_CACHE_TTL: int = 5
    DISABLE_SSL_VERIFY: bool = False

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# issuer همونی که در توکن هست
ISSUER = f"{settings.KEYCLOAK_PUBLIC_URL.rstrip('/')}/realms/{settings.REALM}"

# ولی JWKS و introspect از مسیر داخلی
JWKS_URL = f"{settings.KEYCLOAK_INTERNAL_URL.rstrip('/')}/realms/{settings.REALM}/protocol/openid-connect/certs"
INTROSPECT_URL = f"{settings.KEYCLOAK_INTERNAL_URL.rstrip('/')}/realms/{settings.REALM}/protocol/openid-connect/token/introspect"

app = FastAPI(title="Traefik ForwardAuth - Keycloak JWT Validator")

# ======================
# JWKS CLIENT
# ======================

@lru_cache(maxsize=1)
def get_jwk_client():
    return PyJWKClient(JWKS_URL)


def _validate_with_jwks(token: str):
    jwk_client = get_jwk_client()
    key = jwk_client.get_signing_key_from_jwt(token).key
    payload = jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=settings.CLIENT_ID if settings.CLIENT_ID else None,
        issuer=ISSUER,
        options={"verify_aud": bool(settings.CLIENT_ID)},
        leeway=10,
    )
    return payload


async def introspect_token(token: str) -> dict:
    if not (settings.CLIENT_ID and settings.CLIENT_SECRET):
        raise HTTPException(status_code=500, detail="CLIENT_ID and CLIENT_SECRET required for introspection")

    data = {"token": token}
    auth = (settings.CLIENT_ID, settings.CLIENT_SECRET)

    async with httpx.AsyncClient(verify=not settings.DISABLE_SSL_VERIFY, timeout=5.0) as client:
        try:
            resp = await client.post(INTROSPECT_URL, data=data, auth=auth)
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Introspection request failed: {e}")

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Introspection endpoint returned {resp.status_code}")

    info = resp.json()
    if not info.get("active"):
        raise HTTPException(status_code=401, detail="Token is not active (introspection)")

    return info


async def validate_jwt(token: str) -> dict:
    try:
        return _validate_with_jwks(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.InvalidAudienceError, jwt.InvalidIssuerError) as e:
        raise HTTPException(status_code=403, detail=f"Invalid token claims: {e}")
    except Exception as jwks_err:
        if settings.CLIENT_ID and settings.CLIENT_SECRET:
            try:
                introspect_payload = await introspect_token(token)
                return introspect_payload
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=401, detail=f"Token invalid (jwks+introspect failed): {e}")
        else:
            raise HTTPException(status_code=401, detail=f"Invalid token (JWKS validation failed): {jwks_err}")

# ======================
# ROLE VALIDATION
# ======================

def has_role(payload: dict, required_role: str) -> bool:
    realm_roles = payload.get("realm_access", {}).get("roles", [])
    if required_role in realm_roles:
        return True

    resource_access = payload.get("resource_access", {})
    for client_obj in resource_access.values():
        if required_role in client_obj.get("roles", []):
            return True

    if "roles" in payload and required_role in payload.get("roles", []):
        return True

    scope = payload.get("scope", "")
    if scope and required_role in scope.split():
        return True

    return False

# ======================
# CONFIG LOADER
# ======================

_last_load = 0
_project_config = {}


def get_project_config():
    global _last_load, _project_config
    now = time.time()
    if now - _last_load > settings.CONFIG_CACHE_TTL:
        try:
            with open(settings.CONFIG_FILE, "r") as f:
                data = yaml.safe_load(f) or {}
            _project_config = data.get("projects", {})
            _last_load = now
        except Exception as e:
            print(f"⚠️ Failed to load {settings.CONFIG_FILE}: {e}")
            _project_config = {}
    return _project_config

# ======================
# STARTUP
# ======================

async def safe_get(url: str):authorization layer
    async with httpx.AsyncClient(verify=not settings.DISABLE_SSL_VERIFY) as client:
        return await client.get(url)


@app.on_event("startup")
async def startup_event():
    try:
        resp = await safe_get(JWKS_URL)
        resp.raise_for_status()
        print("✅ JWKS preloaded")
    except Exception as e:
        print(f"⚠️ JWKS preload failed: {e}")

# ======================
# MAIN AUTH ENDPOINT
# ======================

@app.get("/traefik-auth")
async def traefik_auth(request: Request):
    project_name = request.headers.get("x-project-name")
    if not project_name:
        return PlainTextResponse("Missing X-Project-Name header", status_code=400)

    project_config = get_project_config()
    if project_name not in project_config:
        return PlainTextResponse("Unknown project", status_code=403)

    required_roles = project_config[project_name].get("roles", [])

    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return PlainTextResponse("Missing or invalid Authorization header", status_code=401)

    token = auth_header.split(" ")[1]
    payload = await validate_jwt(token)

    if not required_roles:
        return PlainTextResponse("OK", status_code=200)

    if any(has_role(payload, r) for r in required_roles):
        return PlainTextResponse("OK", status_code=200)

    return PlainTextResponse("Forbidden", status_code=403)