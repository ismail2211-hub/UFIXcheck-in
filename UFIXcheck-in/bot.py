import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiosqlite
from datetime import datetime

BOT_TOKEN = "8714366872:AAFmKwU-T2E_JMqDUz_xv23PEko5LeHWfOw"
ADMIN_ID = 5952683615

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

employees = [
    ("#A770", "Abdulloh", "16:00"),
    ("#L470", "Mubina", "00:00"),
    ("#D370", "Davlat", "16:00"),
    ("#D870", "Davron", "08:00"),
    ("#J660", "Laziz", "08:00"),
    ("#P710", "Ibrohim", "00:00"),
    ("#J450", "Yusuf", "16:00"),
    ("#A777", "Bobur", "08:00"),
    ("#C333", "Abdulaziz", "00:00")
]

DB = "attendance.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY,
            employee_id TEXT,
            checkin TEXT,
            checkout TEXT,
            late INTEGER
        )
        """)
        await db.commit()

def keyboard():
    buttons = [[KeyboardButton(text=e[1])] for e in employees]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Выберите своё имя:", reply_markup=keyboard())

@dp.message()
async def checkin(message: types.Message):
    for emp in employees:
        if message.text == emp[1]:
            employee_id = emp[0]
            shift_time = emp[2]

            now = datetime.now()
            shift = datetime.strptime(shift_time, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )

            late = max(int((now - shift).total_seconds() / 60), 0)

            async with aiosqlite.connect(DB) as db:
                await db.execute(
                    "INSERT INTO attendance (employee_id, checkin, late) VALUES (?, ?, ?)",
                    (employee_id, now.isoformat(), late)
                )
                await db.commit()

            if late > 0:
                await message.answer(f"⚠️ Опоздание {late} минут")
            else:
                await message.answer("✅ Check-in выполнен")

            return

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())