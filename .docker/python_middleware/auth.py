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
    KEYCLOAK_HOST: str
    REALM: str
    CLIENT_ID: str | None = None
    JWKS_CACHE_TTL: int = 3600
    CONFIG_FILE: str = "projects.yml"
    CONFIG_CACHE_TTL: int = 5  # seconds
    DISABLE_SSL_VERIFY: bool = True  # useful for mkcert / dev

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

ISSUER = f"{settings.KEYCLOAK_HOST.rstrip('/')}/realms/{settings.REALM}"
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"

app = FastAPI(title="Traefik ForwardAuth - Keycloak JWT Validator")

# ======================
# JWKS CLIENT
# ======================

@lru_cache(maxsize=1)
def get_jwk_client():
    return PyJWKClient(JWKS_URL)


def validate_jwt(token: str):
    jwk_client = get_jwk_client()
    try:
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
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidAudienceError:
        raise HTTPException(status_code=403, detail="Invalid audience")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=403, detail="Invalid issuer")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


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

    return required_role in payload.get("roles", [])


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
# SSL VERIFY (for local mkcert)
# ======================

async def safe_get(url: str):
    """Helper to fetch JWKS ignoring local cert errors if needed."""
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
    payload = validate_jwt(token)

    if not required_roles:
        return PlainTextResponse("OK", status_code=200)

    if any(has_role(payload, r) for r in required_roles):
        return PlainTextResponse("OK", status_code=200)

    return PlainTextResponse("Forbidden", status_code=403)
