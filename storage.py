import aiosqlite
from typing import List, Optional

class Database:
    def __init__(self, path: str = "bot.db"):
        self.path = path
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.path)
        await self.conn.execute("PRAGMA journal_mode=WAL")

    async def setup(self):
        if self.conn is None:
            await self.connect()
        await self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                description TEXT,
                due_date TEXT,
                completed INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT
            );
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event TEXT,
                event_time TEXT
            );
            """
        )
        await self.conn.commit()

    async def add_task(self, user_id: int, description: str, due_date: str):
        await self.conn.execute(
            "INSERT INTO tasks (user_id, description, due_date) VALUES (?, ?, ?)",
            (user_id, description, due_date),
        )
        await self.conn.commit()

    async def list_tasks(self, user_id: int, date: Optional[str] = None) -> List[aiosqlite.Row]:
        cursor = await self.conn.execute(
            "SELECT id, description, due_date, completed FROM tasks WHERE user_id=?" +
            (" AND due_date LIKE ?" if date else ""),
            (user_id, f"{date}%") if date else (user_id,)
        )
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

    async def complete_task(self, user_id: int, task_id: int):
        await self.conn.execute(
            "UPDATE tasks SET completed=1 WHERE user_id=? AND id=?",
            (user_id, task_id),
        )
        await self.conn.commit()

    async def add_note(self, user_id: int, text: str):
        await self.conn.execute(
            "INSERT INTO notes (user_id, text) VALUES (?, ?)",
            (user_id, text),
        )
        await self.conn.commit()

    async def list_notes(self, user_id: int) -> List[aiosqlite.Row]:
        cursor = await self.conn.execute(
            "SELECT id, text FROM notes WHERE user_id=?",
            (user_id,),
        )
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

    async def delete_note(self, user_id: int, note_id: int):
        await self.conn.execute(
            "DELETE FROM notes WHERE user_id=? AND id=?",
            (user_id, note_id),
        )
        await self.conn.commit()

    async def add_event(self, user_id: int, event: str, event_time: str):
        await self.conn.execute(
            "INSERT INTO schedule (user_id, event, event_time) VALUES (?, ?, ?)",
            (user_id, event, event_time),
        )
        await self.conn.commit()

    async def list_events(self, user_id: int) -> List[aiosqlite.Row]:
        cursor = await self.conn.execute(
            "SELECT id, event, event_time FROM schedule WHERE user_id=?",
            (user_id,),
        )
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

    async def delete_event(self, user_id: int, event_id: int):
        await self.conn.execute(
            "DELETE FROM schedule WHERE user_id=? AND id=?",
            (user_id, event_id),
        )
        await self.conn.commit()
