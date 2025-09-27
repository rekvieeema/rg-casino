"""Audit logging service for routing events to a dedicated Telegram chat."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class SupportsSendMessage(Protocol):
    async def send_message(self, chat_id: str | int, text: str) -> None:
        """Protocol for Telegram bot send message method."""


@dataclass(slots=True)
class AuditLogger:
    """Service responsible for delivering audit events to the log chat."""

    bot: SupportsSendMessage
    chat_id: str | int

    async def log(self, message: str) -> None:
        """Send a plain text message to the log chat."""

        await self.bot.send_message(chat_id=self.chat_id, text=message)

    async def user_event(self, user_id: int, message: str) -> None:
        """Log a user scoped event with a consistent prefix."""

        await self.log(f"👤 <code>{user_id}</code>: {message}")

    async def financial_event(self, user_id: int, amount: float, message: str) -> None:
        """Log financial activity with highlighted amount."""

        await self.log(
            f"💰 <code>{user_id}</code>: {message} — <b>{amount:.2f} TON</b>"
        )


__all__ = ["AuditLogger", "SupportsSendMessage"]
