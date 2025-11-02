import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["TG_TOKEN"]
SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:8000")
ADMIN_KEY = os.environ.get("ADMIN_KEY", "change_me")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def queue(pc_id, cmd_type, payload=None):
    headers = {"X-Admin-Key": ADMIN_KEY}
    r = requests.post(f"{SERVER_URL}/command", params={"pc_id": pc_id, "cmd_type": cmd_type}, json=payload or {}, headers=headers, timeout=10)
    return r.json()

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply("Admin bot. Используй /block <pc_id>, /unblock <pc_id>, /run <pc_id> <script>, /update <pc_id>, /wake <pc_id>")

@dp.message_handler(commands=["block"])
async def cmd_block(msg: types.Message):
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 2:
        await msg.reply("Исп: /block <pc_id> [message]")
        return
    pc_id = parts[1]
    payload = {"message": parts[2]} if len(parts) > 2 else {"message":"Этот компьютер заблокирован. Обратитесь к администратору."}
    queue(pc_id, "block", payload)
    await msg.reply(f"Блокировка отправлена: {pc_id}")

@dp.message_handler(commands=["unblock"])
async def cmd_unblock(msg: types.Message):
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.reply("Исп: /unblock <pc_id>")
        return
    pc_id = parts[1]
    queue(pc_id, "unblock", {})
    await msg.reply(f"Разблокировка отправлена: {pc_id}")

@dp.message_handler(commands=["run"])
async def cmd_run(msg: types.Message):
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 3:
        await msg.reply("Исп: /run <pc_id> <script>")
        return
    pc_id = parts[1]
    script = parts[2]
    queue(pc_id, "run_script", {"script": script})
    await msg.reply(f"Скрипт отправлен: {pc_id}")

@dp.message_handler(commands=["update"])
async def cmd_update(msg: types.Message):
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.reply("Исп: /update <pc_id>")
        return
    pc_id = parts[1]
    queue(pc_id, "update", {})
    await msg.reply(f"Команда обновления отправлена: {pc_id}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
