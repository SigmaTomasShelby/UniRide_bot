from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from Commands.create import router as create_router
from db.initDatabase import init_db

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")



bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()

dp.include_router(create_router)

@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    await init_db()
    await message.reply("Здравствуйте! Я бот, созданный для студентов проживающих в НВК. Чем помочь?")



if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))



