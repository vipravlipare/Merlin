"""Compose the local ASGI API while preserving the existing health response.

The caller supplies authentication storage, rate limiting and signing keys.
This module does not load secrets or create connections at import time.
"""

from collections.abc import Callable
import json

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.auth_api import AuthStore, create_auth_app
from app.auth_security import LoginRateLimiter
from app.health_api import default_health_check


def create_api_app(
    *,
    store: AuthStore,
    rate_limiter: LoginRateLimiter,
    signing_key: str | bytes,
    verification_key: str | bytes,
    health_check: Callable[[], object] = default_health_check,
) -> FastAPI:
    """Build one ASGI app with the current health response and auth routes."""
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    @app.exception_handler(RequestValidationError)
    async def invalid_request_handler(_request, _error) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"error": "invalid_request", "message": "Request is invalid"},
        )

    @app.exception_handler(StarletteHTTPException)
    async def route_error_handler(_request, error) -> JSONResponse:
        if error.status_code == 404:
            content = {"error": "not_found", "message": "Not found"}
        elif error.status_code == 405:
            content = {"error": "method_not_allowed", "message": "Method not allowed"}
        else:
            content = {"error": "request_failed", "message": "Request could not be completed"}
        return JSONResponse(status_code=error.status_code, content=content, headers=error.headers)

    @app.get("/health")
    def health() -> Response:
        # Keep the established successful health payload unchanged.
        try:
            body = json.dumps(health_check()).encode("utf-8")
        except Exception:
            body = b'{"error":"Internal server error"}'
            return Response(body, status_code=500, media_type="application/json")
        return Response(body, status_code=200, media_type="application/json")

    # Include the route definitions directly: a root mount would also capture
    # unsupported methods on `/health` before its normal 405 handler runs.
    auth_app = create_auth_app(
        store=store,
        rate_limiter=rate_limiter,
        signing_key=signing_key,
        verification_key=verification_key,
    )
    app.include_router(auth_app.router)
    return app


def run_api_server(
    *,
    store: AuthStore,
    rate_limiter: LoginRateLimiter,
    signing_key: str | bytes,
    verification_key: str | bytes,
) -> None:
    """Run the composed API on loopback after the caller supplies its secrets.

    The existing `python -m app.health_server` command remains a health-only
    server. Application startup code that has loaded real dependencies should
    call this function to serve health and authentication on the same port.
    """
    import uvicorn

    uvicorn.run(
        create_api_app(
            store=store,
            rate_limiter=rate_limiter,
            signing_key=signing_key,
            verification_key=verification_key,
        ),
        host="127.0.0.1",
        port=8000,
        # Forwarded headers are caller-controlled unless a trusted proxy is
        # configured. This learning server binds locally and has no such proxy.
        proxy_headers=False,
    )
