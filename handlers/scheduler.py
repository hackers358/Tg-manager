from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command
from datetime import datetime

from storage import Database

class ScheduleStates(StatesGroup):
    waiting_event = State()
    waiting_time = State()


def register_handlers(dp, db: Database):
    @dp.message_handler(Command('addschedule'))
    async def cmd_addschedule(message: types.Message):
        await message.answer('Введите описание события:')
        await ScheduleStates.waiting_event.set()

    @dp.message_handler(state=ScheduleStates.waiting_event)
    async def event_entered(message: types.Message, state: FSMContext):
        await state.update_data(event=message.text)
        await message.answer('Введите время события (ГГГГ-ММ-ДД ЧЧ:ММ):')
        await ScheduleStates.waiting_time.set()

    @dp.message_handler(state=ScheduleStates.waiting_time)
    async def time_entered(message: types.Message, state: FSMContext):
        try:
            ev_time = datetime.fromisoformat(message.text)
        except ValueError:
            await message.answer('Неверный формат времени. Попробуйте еще раз:')
            return
        data = await state.get_data()
        await db.add_event(message.from_user.id, data['event'], ev_time.isoformat())
        await message.answer('Событие добавлено')
        await state.finish()

    @dp.message_handler(Command('schedule'))
    async def list_schedule(message: types.Message):
        rows = await db.list_events(message.from_user.id)
        if not rows:
            await message.answer('Расписание пусто')
            return
        text = '\n'.join(f"{r['id']}. {r['event']} ({r['event_time']})" for r in rows)
        await message.answer(text)
