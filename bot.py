
import logging
import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils.executor import start_webhook

TOKEN = os.getenv("TOKEN")
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def get_video(url):
    try:
        api_url = f"https://tikwm.com/api/?url={url}"
        response = requests.get(api_url, timeout=10)
        data = response.json()

        if data.get("data"):
            return data["data"]["play"]
        return None
    except:
        return None

@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.reply("👋 Кидай TikTok — скачаю без водяного знаку")

@dp.message_handler()
async def handle_message(message: Message):
    url = message.text.strip()

    if "tiktok.com" not in url:
        await message.reply("❌ Це не TikTok")
        return

    await message.reply("⏳ Завантажую...")

    video = get_video(url)

    if not video:
        await message.reply("❌ Не вдалося скачати")
        return

    try:
        await bot.send_video(message.chat.id, video)
    except:
        await message.reply("⚠️ Помилка")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
    )
