from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from Commands.create import router as create_router
from Commands.find import router as find_router
from db.initDatabase import init_db


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")



bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()

dp.include_router(create_router)
dp.include_router(find_router)

@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    await init_db()
    await message.reply(
                        "Здравствуйте! Меня зовут UniRide, я создан для студентов проживающих в НВК. Помочь добраться домой или подзаработать?\n"
                        "Доступные команды:\n"
                        "/create - создать объявление о поездке, люди которым будет интересно ваше предложение напишут вам в личное сообщение(водитель)\n"
                        "/find - подобрать поездку, можно выбрать такие параметры как время, место отправления и место прибытия(пассажир)\n"
                        "/help - информация о командах доступных командах"
                        )



if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))



