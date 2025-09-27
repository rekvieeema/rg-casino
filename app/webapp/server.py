"""FastAPI application powering the Telegram mini app."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import get_settings


def create_app() -> FastAPI:
    """Return a configured FastAPI application for the mini app."""

    settings = get_settings()
    app = FastAPI(title="RG Casino Mini App", version="0.1.0")

    @app.get("/health", summary="Health check")
    async def health() -> Dict[str, str]:
        return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

    @app.get("/tonconnect-manifest.json", summary="TON Connect manifest")
    async def ton_manifest() -> JSONResponse:
        manifest = {
            "url": str(settings.ton_connect_manifest_url)
            if settings.ton_connect_manifest_url
            else "https://example.com",
            "name": "RG Casino",
            "iconUrl": "https://example.com/icon.png",
            "bridge": {"url": "https://bridge.tonapi.io/bridge"},
            "termsOfUseUrl": "https://example.com/terms",
            "privacyPolicyUrl": "https://example.com/privacy",
        }
        return JSONResponse(manifest)

    @app.get("/leaderboard", summary="Crash game leaderboard")
    async def leaderboard() -> Dict[str, List[Dict[str, str]]]:
        leaders = [
            {"username": "Sinners", "multiplier": "2.08", "reward": "200 TON"},
            {"username": "xoxtil80", "multiplier": "1.50", "reward": "150 TON"},
            {"username": "Rashenorg", "multiplier": "10.31", "reward": "1030 TON"},
        ]
        return {"leaders": leaders}

    return app


app = create_app()


__all__ = ["create_app", "app"]
