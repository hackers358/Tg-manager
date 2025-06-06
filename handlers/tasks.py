from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

from storage import Database

class TaskStates(StatesGroup):
    waiting_description = State()
    waiting_date = State()


def register_handlers(dp, db: Database):
    @dp.message_handler(Command('addtask'))
    async def cmd_addtask(message: types.Message):
        await message.answer('Введите описание задачи:')
        await TaskStates.waiting_description.set()

    @dp.message_handler(state=TaskStates.waiting_description)
    async def task_desc_entered(message: types.Message, state: FSMContext):
        await state.update_data(description=message.text)
        await message.answer('Введите дату и время (ГГГГ-ММ-ДД ЧЧ:ММ):')
        await TaskStates.waiting_date.set()

    @dp.message_handler(state=TaskStates.waiting_date)
    async def task_date_entered(message: types.Message, state: FSMContext):
        try:
            due = datetime.fromisoformat(message.text)
        except ValueError:
            await message.answer('Неверный формат даты. Попробуйте еще раз:')
            return
        data = await state.get_data()
        await db.add_task(message.from_user.id, data['description'], due.isoformat())
        await message.answer('Задача сохранена')
        await state.finish()

    @dp.message_handler(Command('tasks'))
    async def list_tasks(message: types.Message):
        rows = await db.list_tasks(message.from_user.id)
        if not rows:
            await message.answer('Нет задач')
            return
        text = '\n'.join(f"{r['id']}. {'✅' if r['completed'] else '❌'} {r['description']} ({r['due_date']})" for r in rows)
        await message.answer(text)

    @dp.message_handler(Command('donetask'))
    async def done_task(message: types.Message):
        parts = message.text.split()
        if len(parts) < 2 or not parts[1].isdigit():
            await message.answer('Используйте /donetask <id>')
            return
        task_id = int(parts[1])
        await db.complete_task(message.from_user.id, task_id)
        await message.answer('Задача отмечена выполненной')
