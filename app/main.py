"""Composite application launcher for bot and mini app."""

from __future__ import annotations

import asyncio

import uvicorn

from app.bot.main_bot import build_main_bot
from app.webapp import create_app


async def run_bot() -> None:
    bot, dispatcher = await build_main_bot()
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


async def main() -> None:
    """Run bot and web server concurrently (useful for local dev)."""

    config = uvicorn.Config(create_app(), host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    bot_task = asyncio.create_task(run_bot())
    web_task = asyncio.create_task(server.serve())
    await asyncio.wait({bot_task, web_task}, return_when=asyncio.FIRST_COMPLETED)
    for task in (bot_task, web_task):
        if not task.done():
            task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
