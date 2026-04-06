import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.webhook import types as whtypes
import uvicorn
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("BOT_TOKEN required!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("🪖 Джурі Attendance Bot!\n/mark — відмітка\n/view — списки")

@dp.message(Command("mark"))
async def mark(msg: Message):
    await msg.answer("🔒 Введіть пароль: 280911")

@app.post(f"/webhook/bot{TOKEN}")
async def webhook(request: Request):
    update = whtypes.Update(**await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Jura Bot ready 🚀"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
