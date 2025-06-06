import logging
import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from dotenv import load_dotenv

from storage import Database
from handlers import tasks, notes, scheduler
from gpt import ask_gpt
from datetime import datetime, timedelta

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
ALLOWED_USER = int(getenv('USER_ID', 0))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

db = Database()


async def reminder_loop():
    """Periodically check events and send reminders."""
    while True:
        events = await db.list_events(ALLOWED_USER)
        now = datetime.now().replace(second=0, microsecond=0)
        for ev in events:
            ev_time = datetime.fromisoformat(ev['event_time'])
            if now <= ev_time < now + timedelta(minutes=1):
                await bot.send_message(ALLOWED_USER, f"Напоминание: {ev['event']}")
                await db.delete_event(ALLOWED_USER, ev['id'])
        await asyncio.sleep(60)

@dp.message_handler(lambda m: m.from_user.id != ALLOWED_USER)
async def ignore_others(message: types.Message):
    """Ignore messages from other users."""
    return

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    text = (
        "Привет! Я менеджер.\n"
        "Доступные команды:\n"
        "/addtask, /tasks, /donetask\n"
        "/addnote, /notes, /deletenote\n"
        "/addschedule, /schedule\n"
        "/ask <вопрос>"
    )
    await message.answer(text)

@dp.message_handler(commands=['ask'])
async def cmd_ask(message: types.Message):
    query = message.get_args()
    if not query:
        await message.answer('Введите вопрос после /ask')
        return
    response = await ask_gpt(query)
    await message.answer(response)

async def main():
    await db.setup()
    tasks.register_handlers(dp, db)
    notes.register_handlers(dp, db)
    scheduler.register_handlers(dp, db)
    asyncio.create_task(reminder_loop())
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
