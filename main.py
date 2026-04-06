import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import uvicorn

app = FastAPI()
TOKEN = os.getenv('BOT_TOKEN')  # з Render Env
if not TOKEN:
    raise ValueError("BOT_TOKEN NOT SET!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("🪖 Джурі Bot v1.0 ✅\n/mark — відмітка")

@dp.message(Command("mark"))
async def mark(msg: Message):
    await msg.answer("🔒 Введіть пароль: 280911")

# Webhook
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/webhook/bot{TOKEN}")
setup_application(app, dp, bot=bot)

@app.get("/")
async def root():
    return {"status": "Jura Bot READY 🚀", "token_set": bool(TOKEN)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
