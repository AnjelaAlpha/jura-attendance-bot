import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Update, Message
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application  # aiogram 3.x
import asyncio
import uvicorn

load_dotenv()
app = FastAPI()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("🪖 Джурі Bot онлайн!\n/mark — відмітка")

@dp.message(Command("mark"))
async def mark(msg: Message):
    await msg.answer("🔒 Пароль: 280911")

SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/webhook/bot{TOKEN}")
setup_application(app, dp, bot=bot)

@app.get("/")
async def root():
    return {"status": f"Jura Bot v1 (aiogram 3.x) 🚀"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
