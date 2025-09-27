"""Application configuration and settings management."""

from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic import BaseSettings, Field, HttpUrl


class Settings(BaseSettings):
    """Centralised application settings loaded from environment variables."""

    bot_token: str = Field(..., alias="BOT_TOKEN", description="Telegram bot token")
    log_chat_id: str = Field(..., alias="LOG_CHAT_ID", description="Chat ID for logging")
    admin_user_ids: List[int] = Field(
        default_factory=list,
        alias="ADMIN_USER_IDS",
        description="Comma separated list of administrators",
    )

    ton_api_key: Optional[str] = Field(
        default=None,
        alias="TON_API_KEY",
        description="API key for TON Center or other provider",
    )
    ton_network: str = Field(
        default="mainnet",
        alias="TON_NETWORK",
        description="TON network environment: mainnet or testnet",
    )
    ton_connect_manifest_url: Optional[HttpUrl] = Field(
        default=None,
        alias="TON_CONNECT_MANIFEST_URL",
        description="Public URL to TON Connect manifest for the mini app",
    )

    nft_gift_collection: str = Field(
        default="rg-gifts",
        alias="NFT_GIFT_COLLECTION",
        description="Identifier of the NFT collection used for gifts",
    )

    database_url: str = Field(
        default="sqlite+aiosqlite:///./casino.db",
        alias="DATABASE_URL",
        description="Database URL used for storing user balances and bets",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = ","


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()


__all__ = ["Settings", "get_settings"]
