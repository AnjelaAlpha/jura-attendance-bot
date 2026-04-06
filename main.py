import os, json
from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.types import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import uvicorn
from datetime import datetime

app = FastAPI()
TOKEN = os.getenv('BOT_TOKEN')
bot_data = {}  # {chat_id: {"riy": str, "selected": set()}}

# Учасники роїв (з вашого опису)
gen_members = [
    "Панько Анастасія", 
    "Маковецький Павло", 
    "Шимановський Денис", 
    "Іконська Дар\'я", 
    "Новохацька Марія", 
    "Драга Софія", 
    "Дрібко Максим", 
    "Фурсенко Анна", 
    "Дзяхар Анастасія", 
    "Людвенко Поліна", 
    "Новохацька Валерія", 
    "Терлецький Дмитро"
]

gro_members = [
    "Гедзун Данило",
    "Черпак Ростислав", 
    "Панько Анастасія",
    "Котік Вікторія", 
    "Кузьменчук Ілля",
    "Однорог Антон",
    "Мітлицька Анастасія",
    "Розгон Дар\'я",
    "Харченко Анна"
]

def get_users_kb(riy, selected):
    members = gen_members if riy == 'gen' else gro_members
    kb = []
    for member in members:
        mark = "✅ " if member in selected else ""
        kb.append([InlineKeyboardButton(f"{mark}{member}", callback_data=f"user:{riy}:{member}")])
    kb.append([InlineKeyboardButton("✅ Завершити відмітку", callback_data="finish_mark")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

riy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Генерація гідності♥️", callback_data="riy:gen")],
    [InlineKeyboardButton("Грозові крила", callback_data="riy:gro")]
])

async def process_update(data):
    chat_id = data.get("message", {}).get("chat", {}).get("id") or data.get("callback_query", {}).get("message", {}).get("chat", {}).get("id")

    if not chat_id:
        return

    if "message" in data:
        msg = data["message"]
        text = msg.get("text", "")
        if text == "/start":
            await bot.send_message(chat_id, "🪖 Джурі Attendance Bot FULL\n\n📝 /mark - відмітка присутніх")
        elif text == "/mark":
            await bot.send_message(chat_id, "🎯 Учасників якого рою відмітити?", reply_markup=riy_kb)
        elif text == "280911":
            await bot.send_message(chat_id, "✅ Авторизовано! /mark для відмітки")

    elif "callback_query" in data:
        cb = data["callback_query"]
        msg_id = cb["message"]["message_id"]
        await bot.answer_callback_query(cb["id"])

        data_parts = cb["data"].split(":")

        if data_parts[0] == "riy":
            riy = data_parts[1]
            bot_data[chat_id] = {"riy": riy, "selected": set()}
            kb = get_users_kb(riy, set())
            await bot.edit_message_text("✅ Відмічайте присутніх:", chat_id, msg_id, reply_markup=kb)

        elif data_parts[0] == "user":
            riy = data_parts[1]
            user = ":".join(data_parts[2:])
            if chat_id in bot_data:
                selected = bot_data[chat_id]["selected"]
                if user in selected:
                    selected.remove(user)
                else:
                    selected.add(user)
                kb = get_users_kb(bot_data[chat_id]["riy"], selected)
                await bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=kb)

        elif cb["data"] == "finish_mark":
            if chat_id in bot_data:
                state = bot_data[chat_id]
                riy_name = "Генерація гідності♥️" if state["riy"] == "gen" else "Грозові крила"
                count = len(state["selected"])
                total = len(gen_members if state["riy"] == "gen" else gro_members)
                date_str = datetime.now().strftime("%d.%m.%Y")
                await bot.send_message(chat_id, f"✅ Відмітка завершена!\n\n🏷️ Рій: {riy_name}\n📅 Дата: {date_str}\n👥 Присутні: {count}/{total}")
                del bot_data[chat_id]

@app.post(f"/webhook/bot{TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    await process_update(data)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Jura Attendance Bot FULL READY 🚀", "features": "marking, multi-select, roys"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
