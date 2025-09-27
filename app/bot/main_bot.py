"""Main Telegram bot configuration and entrypoint."""

from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.config import get_settings
from app.services import AuditLogger, CasinoEngine

from .router import build_router, build_storage
from .views import BotContext, default_cases


async def build_main_bot() -> tuple[Bot, Dispatcher]:
    """Configure and return the bot with dispatcher ready to be polled."""

    settings = get_settings()
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    storage = build_storage()
    dispatcher = Dispatcher(storage=storage)

    router = build_router()
    dispatcher.include_router(router)

    audit_logger = AuditLogger(bot=bot, chat_id=settings.log_chat_id)
    casino_engine = CasinoEngine()
    context_middleware = _ContextMiddleware(audit_logger, casino_engine)

    router.message.middleware.register(context_middleware)
    router.callback_query.middleware.register(context_middleware)

    return bot, dispatcher


class _ContextMiddleware:
    """Simple middleware injecting BotContext into handler kwargs."""

    def __init__(self, audit_logger: AuditLogger, casino: CasinoEngine) -> None:
        self._audit_logger = audit_logger
        self._casino = casino
        self._cases = default_cases()

    async def __call__(self, handler, event, data):  # type: ignore[override]
        data["bot_context"] = BotContext(
            audit_logger=self._audit_logger, casino=self._casino, cases=self._cases
        )
        return await handler(event, data)


async def main() -> None:
    """Entrypoint for running polling from command line."""

    bot, dispatcher = await build_main_bot()
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
