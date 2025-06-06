from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command

from storage import Database

class NoteStates(StatesGroup):
    waiting_text = State()


def register_handlers(dp, db: Database):
    @dp.message_handler(Command('addnote'))
    async def cmd_addnote(message: types.Message):
        await message.answer('Введите текст заметки:')
        await NoteStates.waiting_text.set()

    @dp.message_handler(state=NoteStates.waiting_text)
    async def note_text_entered(message: types.Message, state: FSMContext):
        await db.add_note(message.from_user.id, message.text)
        await message.answer('Заметка сохранена')
        await state.finish()

    @dp.message_handler(Command('notes'))
    async def list_notes(message: types.Message):
        rows = await db.list_notes(message.from_user.id)
        if not rows:
            await message.answer('Нет заметок')
            return
        text = '\n'.join(f"{r['id']}. {r['text']}" for r in rows)
        await message.answer(text)

    @dp.message_handler(Command('deletenote'))
    async def delete_note(message: types.Message):
        parts = message.text.split()
        if len(parts) < 2 or not parts[1].isdigit():
            await message.answer('Используйте /deletenote <id>')
            return
        note_id = int(parts[1])
        await db.delete_note(message.from_user.id, note_id)
        await message.answer('Заметка удалена')
