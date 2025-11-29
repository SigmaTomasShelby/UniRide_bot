from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram import types
import sqlite3

router = Router()

class FindForm(StatesGroup):
    find_time = State()
    find_from_place = State()
    find_to_place = State()

@router.message(Command("find"))
async def cmd_create(message: Message, state: FSMContext):
    await state.set_state(FindForm.find_time)
    await message.answer("🕐 Введите дату и время поездки через пробел(например, 28.11.25 18:30):")

@router.message(FindForm.find_time)
async def process_time(message: Message, state: FSMContext):
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
    await message.answer(
        f"🕐 Время: {data['find_time']}\n"
        f"📍 Откуда: {data['find_from_place']}\n"
        f"📍 Куда: {data['find_to_place']}"
    )
    
    await state.clear()
