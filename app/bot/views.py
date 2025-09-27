"""Message and callback handlers for the Telegram casino bot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from aiogram.enums import ParseMode
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.config import get_settings
from app.services import AuditLogger, CasinoEngine, Case, CaseItem

settings = get_settings()


@dataclass(slots=True)
class BotContext:
    """Container used to pass shared services into handlers."""

    audit_logger: AuditLogger
    casino: CasinoEngine
    cases: Dict[str, Case]


def _build_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Играть", callback_data="action:play")],
            [InlineKeyboardButton(text="💎 Кейсы", callback_data="action:cases")],
            [InlineKeyboardButton(text="💳 Пополнить", callback_data="action:deposit")],
            [InlineKeyboardButton(text="📤 Вывод", callback_data="action:withdraw")],
        ]
    )


async def start(message: Message, bot_context: BotContext) -> None:
    """Handle the /start command."""

    await bot_context.audit_logger.user_event(message.from_user.id, "зашёл в бота")
    await message.answer(
        "🚀 Добро пожаловать в RG Casino!\n"
        "Здесь вас ждёт краш-игра на TON и NFT подарки.",
        reply_markup=_build_main_keyboard(),
    )


class ProfileFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text == "Профиль"


async def show_profile(message: Message, bot_context: BotContext) -> None:
    balance = 0.0
    await message.answer(
        "👤 Профиль\n"
        f"ID: <code>{message.from_user.id}</code>\n"
        f"Баланс: <b>{balance:.2f} TON</b>\n"
        "Подключите TON кошелёк через mini app для пополнения",
        parse_mode=ParseMode.HTML,
        reply_markup=_build_main_keyboard(),
    )


class CasesFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text == "Кейсы"


async def show_cases(message: Message, bot_context: BotContext) -> None:
    lines = ["🎁 Доступные кейсы:"]
    for case in bot_context.cases.values():
        lines.append(
            f"• <b>{case.title}</b> — {case.price:.2f} TON"
        )
    await message.answer("\n".join(lines), parse_mode=ParseMode.HTML)


class DepositCallbackFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "action:deposit"


async def handle_deposit(callback: CallbackQuery, bot_context: BotContext) -> None:
    await bot_context.audit_logger.user_event(
        callback.from_user.id, "открыл меню пополнения"
    )
    await callback.message.answer(
        "Пополнение через TON Connect готово.\n"
        "Нажмите кнопку ниже чтобы открыть mini app.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔗 Открыть TON Connect",
                        url=str(settings.ton_connect_manifest_url)
                        if settings.ton_connect_manifest_url
                        else "https://ton.app",
                    )
                ]
            ]
        ),
    )
    await callback.answer()


class WithdrawCallbackFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "action:withdraw"


async def handle_withdraw(callback: CallbackQuery, bot_context: BotContext) -> None:
    await bot_context.audit_logger.user_event(
        callback.from_user.id, "запросил вывод средств"
    )
    await callback.message.answer(
        "Введите адрес кошелька TON в чате. Оператор проверит заявку и отправит NFT подарок.",
    )
    await callback.answer()


def default_cases() -> Dict[str, Case]:
    """Default configuration of loot cases inspired by design mockups."""

    starter_case = Case(
        title="Starter Rocket",
        price=0.1,
        items=[
            CaseItem(title="🚀 x1.1", probability=0.6, reward=0.11, emoji="🚀"),
            CaseItem(title="🌕 x1.5", probability=0.3, reward=0.15, emoji="🌕"),
            CaseItem(title="💎 NFT", probability=0.1, reward=0.5, emoji="💎"),
        ],
    )
    epic_case = Case(
        title="Epic Galaxy",
        price=0.5,
        items=[
            CaseItem(title="⭐ x1.2", probability=0.5, reward=0.6, emoji="⭐"),
            CaseItem(title="🔥 x2.0", probability=0.3, reward=1.0, emoji="🔥"),
            CaseItem(title="👑 NFT", probability=0.2, reward=2.5, emoji="👑"),
        ],
    )
    return {"starter": starter_case, "epic": epic_case}


__all__ = [
    "BotContext",
    "start",
    "show_profile",
    "show_cases",
    "handle_deposit",
    "handle_withdraw",
    "default_cases",
    "ProfileFilter",
    "CasesFilter",
    "DepositCallbackFilter",
    "WithdrawCallbackFilter",
]
