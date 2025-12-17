from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram import types
import sqlite3
from application.checker import Checker
from application.offerFinder import find_offers

router = Router()

class FindForm(StatesGroup):
    find_time = State()
    find_from_place = State()
    find_to_place = State()
    start_finding = State()

@router.message(Command("find"))
async def cmd_create(message: Message, state: FSMContext):
    await state.set_state(FindForm.find_time)
    await message.answer("🕐 Введите дату и время поездки через пробел(например, 28.11.25 18:30):")

@router.message(FindForm.find_time)
async def process_time(message: Message, state: FSMContext):
    date_str = message.text.strip()
    
    if not Checker.check_date(date_str):
        await message.answer(
            "❌ **Неверная дата или время в прошлом!**\n"
            "🕐 Введите дату и время поездки в будущем:\n"
            "Формат: `28.11.26 18:30`",
            parse_mode="Markdown"
        )
        return
    await state.update_data(find_time=message.text)
    await state.set_state(FindForm.find_from_place)
    await message.answer("📍 Откуда вы едете?")

@router.message(FindForm.find_from_place)
async def process_from_place(message: Message, state: FSMContext):
    await state.update_data(find_from_place=message.text)
    await state.set_state(FindForm.find_to_place)
    await message.answer("📍 Куда вы едете?")

@router.message(FindForm.find_to_place)
async def process_to_place(message: Message, state: FSMContext):
    await state.update_data(find_to_place=message.text)
    
    data = await state.get_data()
    
    trip_time = data["find_time"]
    from_place = data["find_from_place"]
    to_place = data["find_to_place"]

    offers = find_offers(trip_time, from_place, to_place)

    if not offers:
        await message.answer(
            "❌ Подходящих заявок не найдено.\n"
            "Попробуйте изменить время или места отправления/прибытия."
        )
        await state.clear()
        return

    text_lines = []
    for (
        username,
        name,
        time_of_start,
        place_of_departure,
        place_of_arrival,
        cost,
        comment,
    ) in offers:
        text_lines.append(
            "🚗 Найдена заявка:\n"
            f"👤 Имя: {name} ({username})\n"
            f"🕐 Время отправления: {time_of_start}\n"
            f"📍 Откуда: {place_of_departure}\n"
            f"📍 Куда: {place_of_arrival}\n"
            f"💰 Стоимость: {cost}\n"
            f"💬 Комментарий: {comment or '—'}"
        )

    result_text = "\n\n".join(text_lines)

    await message.answer(
        "Вот найденные заявки по вашему запросу:\n\n" + result_text
    )

    await state.clear()
