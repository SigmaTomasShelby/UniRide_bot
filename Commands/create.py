from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram import types

router = Router()

class TripForm(StatesGroup):
    name = State()
    time = State()
    from_place = State()
    to_place = State()
    cost = State()
    comment = State()

@router.message(Command("create"))
async def cmd_create(message: Message, state: FSMContext):
    await state.set_state(TripForm.name)
    await message.answer("👤 Введите ваше имя:")

@router.message(TripForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(TripForm.time)
    await message.answer("🕐 Введите дату и время поездки через пробел(например, 28.11.25 18:30):")

@router.message(TripForm.time)
async def process_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(TripForm.from_place)
    await message.answer("📍 Откуда вы едете?")

@router.message(TripForm.from_place)
async def process_from_place(message: Message, state: FSMContext):
    await state.update_data(from_place=message.text)
    await state.set_state(TripForm.to_place)
    await message.answer("📍 Куда вы едете?")

@router.message(TripForm.to_place)
async def process_to_place(message: Message, state: FSMContext):
    await state.update_data(to_place=message.text)
    await state.set_state(TripForm.cost)
    await message.answer("💰 Введите стоимость поездки:")

@router.message(TripForm.cost)
async def process_cost(message: Message, state: FSMContext):
    await state.update_data(cost=message.text)
    await state.set_state(TripForm.comment)
    await message.answer("💬 Добавьте комментарий (или /skip):")

@router.message(F.text == "/skip", TripForm.comment)
@router.message(TripForm.comment)
async def process_comment(message: Message, state: FSMContext):
    comment = message.text if message.text != "/skip" else ""
    await state.update_data(comment=comment)
    username = "@" + message.from_user.username
    
    data = await state.get_data()
    await message.answer(
        f"✅ **Анкета создана!**\n\n"
        f"** USERNAME: {username}\n"
        f"👤 **Имя:** {data['name']}\n"
        f"🕐 **Дата и время:** {data['time']}\n"
        f"📍 **Откуда:** {data['from_place']}\n"
        f"📍 **Куда:** {data['to_place']}\n"
        f"💰 **Стоимость:** {data['cost']}\n"
        f"💬 **Комментарий:** {data['comment']}",
        parse_mode="Markdown"
    )
    await state.clear()
