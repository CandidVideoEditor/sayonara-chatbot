from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
import random
import os
import asyncio
import datetime

# ---------------- CONFIG ---------------- #

API_ID = 14050586
API_HASH = "42a60d9c657b106370c79bb0a8ac560c"
BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URL = "mongodb+srv://vipboy:vipboy@vipboy.hfa8bzb.mongodb.net/?retryWrites=true&w=majority"

CREATOR_ID = 8432556224   # FULL ACCESS OWNER

bot = Client(
    "AI_CHATBOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

db = MongoClient(MONGO_URL)
chatdb = db["CHATBOT"]
memory = chatdb["MEMORY"]
settings = chatdb["SETTINGS"]

# ---------------- UTILS ---------------- #

def is_creator(user_id):
    return user_id == CREATOR_ID


def get_username(user):
    if user.first_name:
        return user.first_name
    return "Buddy"


def random_emoji():
    return random.choice(["😄", "🔥", "😎", "🥰", "✨", "🤍", "😜"])


def smart_reply(text):
    """Multi-language casual AI style"""
    replies = [
        f"{text} 😄",
        f"Arre wah! {text} 🔥",
        f"Super da 😎 {text}",
        f"Ayyo 😅 {text}",
        f"Niceee 😍 {text}",
        f"Cool bro 😎 {text}",
    ]
    return random.choice(replies)


# ---------------- START COMMAND ---------------- #

@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    name = get_username(message.from_user)
    await message.reply_text(
        f"👋 Hey {name}!\n\n"
        "🤖 I'm your **Smart AI ChatBot**\n"
        "I talk like humans 😎\n"
        "I understand *English / Hinglish / Tanglish / Telugu mix*\n\n"
        "💬 Just start chatting!\n"
        "🎧 Voice | 😄 Stickers | 🔥 Trending talks supported\n"
    )


# ---------------- MAIN CHAT LOGIC ---------------- #

@bot.on_message(filters.text & ~filters.bot)
async def chat_handler(client, message: Message):

    user = message.from_user
    text = message.text.lower()

    # Save chat
    memory.insert_one({
        "user": user.id,
        "text": text,
        "time": datetime.datetime.now()
    })

    # Greeting detection
    if any(x in text for x in ["hi", "hello", "hey", "yo"]):
        return await message.reply_text(
            f"Hey {user.first_name} 😄 How are you da?"
        )

    # Mood replies
    if "sad" in text or "depressed" in text:
        return await message.reply_text(
            "Ayyo 😔 Don't worry ra… I'm here for you ❤️"
        )

    if "love" in text:
        return await message.reply_text(
            "Awww ❤️ Love is in the air 😌"
        )

    if "who are you" in text:
        return await message.reply_text(
            "I'm your friendly AI buddy 🤖✨"
        )

    # Trending talk mock
    if "news" in text or "trending" in text:
        return await message.reply_text(
            "🔥 Trending now:\n• AI taking over 😎\n• Movies rocking 🎬\n• India winning everywhere 🇮🇳"
        )

    # Default AI talk
    await message.reply_text(
        smart_reply(text)
    )


# ---------------- STICKER REPLY ---------------- #

@bot.on_message(filters.sticker)
async def sticker_reply(client, message: Message):
    await message.reply_sticker(message.sticker.file_id)


# ---------------- CREATOR COMMAND ---------------- #

@bot.on_message(filters.command("creator"))
async def creator_info(client, message: Message):
    if message.from_user.id == CREATOR_ID:
        await message.reply_text("👑 You are the CREATOR of this bot.")
    else:
        await message.reply_text("⚠️ Only creator can access this.")


# ---------------- RUN ---------------- #

print("🤖 AI CHATBOT IS RUNNING...")
bot.run()
