"""Telegram router configuration for the main bot."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

from . import views


def build_router() -> Router:
    """Create the main router with all handlers registered."""

    router = Router(name="main")
    router.message.register(views.start, CommandStart())
    router.message.register(views.show_profile, views.ProfileFilter())
    router.message.register(views.show_cases, views.CasesFilter())
    router.callback_query.register(views.handle_deposit, views.DepositCallbackFilter())
    router.callback_query.register(views.handle_withdraw, views.WithdrawCallbackFilter())
    return router


def build_storage() -> MemoryStorage:
    """Return in-memory FSM storage used by the bot."""

    return MemoryStorage()


__all__ = ["build_router", "build_storage"]
