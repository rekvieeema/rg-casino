# RG Casino

Телеграм-казино на TON с NFT подарками и mini app.

## Возможности

- 🚀 Краш-игра с динамическим множителем
- 💎 Лутбоксы/кейсы с NFT наградами
- 💳 Пополнение через TON Connect и подарки
- 📤 Вывод с логированием в отдельный чат
- 📊 Мини-приложение на FastAPI для интеграции в Telegram mini apps

## Архитектура

```
app/
├── bot/              # Основной Telegram бот (aiogram v3)
├── services/         # Движок казино, логирование, бизнес-логика
├── ton/              # Обертка над TON API
└── webapp/           # FastAPI mini app (TON Connect manifest, лидерборд)
```

- **Основной бот** обслуживает игроков, запускает мини-игры и вызывает `AuditLogger` для записи событий в чат логов.
- **Log-чат** получает все события (`запуск`, `пополнение`, `заявка на вывод`).
- **FastAPI mini app** хранит manifest для TON Connect и может отдавать лидерборд.

## Подготовка окружения

1. Скопируйте `.env.example` в `.env` и укажите токены.
2. Установите зависимости через [Poetry](https://python-poetry.org/):

   ```bash
   poetry install
   ```

3. Активируйте виртуальное окружение Poetry:

   ```bash
   poetry shell
   ```

## Переменные окружения

| Переменная | Описание |
| ---------- | -------- |
| `BOT_TOKEN` | Токен Telegram бота (от @BotFather) |
| `LOG_CHAT_ID` | ID чата или канала, куда писать логи |
| `ADMIN_USER_IDS` | Список ID админов (через запятую) |
| `TON_API_KEY` | Ключ API toncenter (опционально) |
| `TON_NETWORK` | `mainnet` или `testnet` |
| `TON_CONNECT_MANIFEST_URL` | Публичная ссылка на manifest mini app |
| `NFT_GIFT_COLLECTION` | Коллекция NFT подарков |
| `DATABASE_URL` | БД для балансов (по умолчанию SQLite) |

## Запуск бота

```bash
poetry run python -m app.bot.main_bot
```

## Запуск mini app (FastAPI)

```bash
poetry run uvicorn app.webapp.server:app --reload
```

После запуска доступен manifest по адресу `http://127.0.0.1:8000/tonconnect-manifest.json`.

## Развитие

- Подключить реальную БД (PostgreSQL) для балансов и истории ставок
- Реализовать TON Connect фронтенд и NFT подарки
- Добавить поддержку mini app UI (React/Next.js) поверх FastAPI
- Настроить CI/CD и деплой в облако (Railway/Render/DO)
