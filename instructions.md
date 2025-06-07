# 🤖 Проект: Telegram-бот-помощник с памятью и базой знаний на Supabase

## Цель
Создать умного ассистента, работающего через Telegram с использованием GPT. Все данные хранятся в Supabase, что обеспечивает устойчивую память и возможность организации задач, заметок и событий. Бот должен вести себя как полноценный ассистент, способный запоминать детали переписки и автоматически сохранять их в соответствующие таблицы базы данных.

## Возможности
- Сохранение истории сообщений, заметок, задач, напоминаний, событий и привычек.
- Ответы с учётом контекста переписки (таблица `messages`).
- Использование таблицы `memory_chunks` для долговременной памяти.
- Создание и управление напоминаниями, привычками и задачами напрямую через диалог.
- Автоматическое определение, в какую таблицу стоит записать новую информацию.

## Структура таблиц Supabase
1. **users** – `id`, `name`, `style`, `mode`, `timezone`, `created_at`
2. **messages** – `user_id`, `text`, `response`, `created_at`
3. **notes** – `user_id`, `note`, `created_at`
4. **memory_chunks** – `user_id`, `topic`, `content`, `source`, `created_at`
5. **tasks** – `user_id`, `title`, `description`, `status`, `due_date`, `created_at`
6. **reminders** – `user_id`, `message`, `remind_at`, `is_sent`, `created_at`
7. **events** – `user_id`, `title`, `description`, `location`, `start_time`, `end_time`, `created_at`
8. **habits** – `user_id`, `title`, `description`, `frequency`, `start_date`, `is_active`, `created_at`
9. **habits_logs** – `habit_id`, `user_id`, `log_date`, `status`, `created_at`

## Основные файлы
- `bot.py` – логика Telegram-бота и работа с GPT.
- `config.py` – конфигурация (ключи API: `openai_api_key`, `supabase_url`, `supabase_key`, `telegram_token`).
- `requirements.txt` – зависимости `python-telegram-bot`, `openai`, `supabase`.

## Запуск
```bash
pip install -r requirements.txt
python bot.py
```

GPT должен сохранять важные сведения в Supabase и вести себя как личный ассистент. Он понимает названия таблиц и самостоятельно формирует SQL-запросы для их заполнения.
