import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import os
import aiohttp

TOKEN = os.getenv("TG_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")
ADMIN_KEY = os.getenv("ADMIN_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("✅ Бот запущен. Используй /lock или /unlock.")

@dp.message(Command("lock"))
async def lock_handler(message: Message):
    pc_id = "A101-PC01"  # можно сделать динамическим
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{SERVER_URL}/lock", json={"pc_id": pc_id, "admin_key": ADMIN_KEY}) as resp:
            if resp.status == 200:
                await message.answer(f"💻 ПК {pc_id} заблокирован")
            else:
                await message.answer("❌ Ошибка при блокировке")

@dp.message(Command("unlock"))
async def unlock_handler(message: Message):
    pc_id = "A101-PC01"
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{SERVER_URL}/unlock", json={"pc_id": pc_id, "admin_key": ADMIN_KEY}) as resp:
            if resp.status == 200:
                await message.answer(f"🔓 ПК {pc_id} разблокирован")
            else:
                await message.answer("❌ Ошибка при разблокировке")

async def main():
    print("Бот запущен 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
