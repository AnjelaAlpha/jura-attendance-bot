import os, json
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import uvicorn
from datetime import datetime

app = FastAPI()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class MarkFSM(StatesGroup):
    riy = State()
    users = State()
    event = State()

riy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Генерація гідності♥️", callback_data="riy:gen")],
    [InlineKeyboardButton("Грозові крила", callback_data="riy:gro")]
])

@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("🪖 Джурі Bot v2.1 ✅\n/mark — відмітка\n/view — списки")

@dp.message(Command("mark"))
async def mark_start(msg: Message, state: FSMContext):
    await msg.answer("Рій?", reply_markup=riy_kb)
    await state.set_state(MarkFSM.riy)

@dp.callback_query(F.data.startswith("riy:"))
async def select_riy(callback: CallbackQuery, state: FSMContext):
    riy = "gen" if "gen" in callback.data else "gro"
    await state.update_data(riy=riy)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("✅ Завершити", callback_data="finish_users")],
        [InlineKeyboardButton("👤 Показати список", callback_data="show_users")]
    ])
    await callback.message.edit_text(f"Відмічайте {riy}...", reply_markup=kb)
    await state.set_state(MarkFSM.users)

async def handle_update(update: Update):
    await dp.feed_update(bot, update)

@app.post(f"/webhook/bot{TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await handle_update(update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Jura Bot v2.1 LIVE 🚀"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
