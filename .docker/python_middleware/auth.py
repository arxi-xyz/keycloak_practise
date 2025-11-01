import requests
from jose import jwt, jwk
from jose.exceptions import JWTError, ExpiredSignatureError
from jose.utils import base64url_decode
from cachetools import TTLCache
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
from pydantic import Field

# --------------------------
# Config
# --------------------------


class Settings(BaseSettings):
    keycloak_public_url: str
    keycloak_internal_url: str
    realm: str
    client_id: str = Field(..., alias="AUTH_CLIENT_ID")
    client_secret: str = Field(..., alias="AUTH_CLIENT_SECRET")
    jwks_cache_ttl: int = 3600
    config_file: str = "projects.yml"
    config_cache_ttl: int = 5

    class Config:
        env_file = ".env"
        populate_by_name = True


settings = Settings()


# --------------------------
# JWKS Cache
# --------------------------
_jwks_cache = TTLCache(maxsize=1, ttl=settings.jwks_cache_ttl)


def get_jwks():
    """Fetch JWKS from Keycloak or cache"""
    if "jwks" in _jwks_cache:
        return _jwks_cache["jwks"]

    url = f"{settings.keycloak_internal_url}/realms/{settings.realm}/protocol/openid-connect/certs"
    resp = requests.get(url)
    resp.raise_for_status()
    jwks = resp.json()
    _jwks_cache["jwks"] = jwks
    return jwks


# --------------------------
# JWT Validator
# --------------------------
def validate_jwt(token: str):
    """Validate JWT using Keycloak's JWKS"""
    try:
        header = jwt.get_unverified_header(token)
    except JWTError:
        raise ValueError("unauthorized")

    kid = header.get("kid")
    
    jwks = get_jwks()
    key_data = next((k for k in jwks["keys"] if k["kid"] == kid), None)
    if not key_data:
        raise ValueError("unauthorized")

    public_key = jwk.construct(key_data)
    try:
        message, encoded_sig = token.rsplit(".", 1)
        decoded_sig = base64url_decode(encoded_sig.encode())
        if not public_key.verify(message.encode(), decoded_sig):
            raise ValueError("unauthorized")
    except Exception:
        raise ValueError("unauthorized")

    try:
        decoded = jwt.decode(
            token,
            public_key.to_pem().decode(),
            algorithms=[key_data.get("alg", "RS256")],
            audience=settings.client_id,
            options={"verify_exp": True},
        )
        return decoded
    except ExpiredSignatureError:
        raise ValueError("unauthorized")
    except JWTError as e:
        raise ValueError(f"unauthorized")



# --------------------------
# FastAPI App
# --------------------------
app = FastAPI(title="JWT Validation Gateway")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing or invalid Authorization header"},
        )

    token = auth_header.split(" ")[1]

    try:
        decoded = validate_jwt(token)
    except ValueError as e:
        return JSONResponse(status_code=401, content={"detail": str(e)})

    # Extract claims
    user_id = decoded.get("sub")
    username = decoded.get("preferred_username")
    project = decoded.get("project", "default")
    roles = decoded.get("realm_access", {}).get("roles", [])

    # Inject headers
    request.state.forward_headers = {
        "X-Forwarded-UserId": user_id or "",
        "X-Forwarded-User": username or "",
        "X-Forwarded-Project": project,
        "X-Forwarded-Roles": ",".join(roles),
    }

    response = await call_next(request)
    for k, v in request.state.forward_headers.items():
        response.headers[k] = v
    return response


@app.get("/validate")
async def validate(request: Request):
    headers = getattr(request.state, "forward_headers", None)
    if not headers:
        raise HTTPException(status_code=401, detail="No valid user context found.")
    return {"valid": True, "headers": headers}