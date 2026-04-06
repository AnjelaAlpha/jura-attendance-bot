import os, json
from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.types import Update, Message
from aiogram.filters import Command
import uvicorn
import asyncio

app = FastAPI()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)

async def handle_update(update: Update):
    if update.message:
        msg = update.message
        if msg.text == '/start':
            await bot.send_message(msg.chat.id, "🪖 Джурі Bot v2.0 ✅\n/mark — відмітка")
        elif msg.text == '/mark':
            await bot.send_message(msg.chat.id, "🔒 Пароль: 280911")
        else:
            await bot.send_message(msg.chat.id, "Невідома команда. /start")

@app.post(f"/webhook/bot{TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await handle_update(update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Jura Bot LIVE 🚀"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
