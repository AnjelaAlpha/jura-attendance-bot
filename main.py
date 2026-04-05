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
bot = Bot(token=TOKEN)
dp = Dispatcher()

@app.post(f"/webhook/bot{TOKEN}")
async def webhook(request: Request):
    update = whtypes.Update(**await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}

@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("🪖 Джурі Bot готовий!\n/mark — скоро")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
