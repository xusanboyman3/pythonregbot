import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, Column, Integer, String
from keep_alive import keep_alive
import re
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.testing.provision import create_db

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///dp.sqlite3"
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)
Base = declarative_base()
API_TOKEN = '7234794963:AAEdW_vwTBEAqTBSRGVJk2bXB5LKzrNiSUg'
bot = Bot(token=API_TOKEN)
# Keyboards
language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 Uz"), KeyboardButton(text='🇷🇺 Ru')]
    ], resize_keyboard=True, one_time_keyboard=True
)

confirm_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='✅ Tastiqlayman')],
        [KeyboardButton(text='Qaytatan')]
    ], resize_keyboard=True,
    one_time_keyboard=True
)

confirm_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='✅ Я подтверждаю')],
        [KeyboardButton(text='Назад ↩️')]
    ], resize_keyboard=True,
    one_time_keyboard=True
)

contact_keyboard_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Telefon raqamni ulashish", request_contact=True), KeyboardButton(text='Orqaga ↩️')]
    ], resize_keyboard=True, one_time_keyboard=True
)

contact_keyboard_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Поделиться номером телефона", request_contact=True), KeyboardButton(text='Назад ↩️')]
    ], resize_keyboard=True, one_time_keyboard=True
)

back_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Orqaga ↩️")]
    ], resize_keyboard=True, one_time_keyboard=True
)

back_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Назад ↩️")]
    ], resize_keyboard=True, one_time_keyboard=True
)

yes_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Yo'q"), KeyboardButton(text="Ha")]
    ], resize_keyboard=True, one_time_keyboard=True
)

yes_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Нет"), KeyboardButton(text="Да")]
    ], resize_keyboard=True, one_time_keyboard=True
)

skip_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="▶️ O‘tkazib yuborish"), KeyboardButton(text="Orqaga ↩️")]
    ], resize_keyboard=True, one_time_keyboard=True
)

skip_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Назад ↩️"), KeyboardButton(text="▶️ Пропустить")]
    ], resize_keyboard=True, one_time_keyboard=True
)

register_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Anketa to'ldirish 📝")]
    ], resize_keyboard=True, one_time_keyboard=False
)

register_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Заполнить анкету 📝")]
    ], resize_keyboard=True, one_time_keyboard=False
)

gender_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨 Erkak️"), KeyboardButton(text="👩‍🦰 Ayol")],
        [KeyboardButton(text="Orqaga ↩️")]
    ], resize_keyboard=True, one_time_keyboard=True
)

gender_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨 Мужчина️"), KeyboardButton(text="👩‍🦰 Женщина")],
        [KeyboardButton(text="Назад ↩️")]
    ], resize_keyboard=True, one_time_keyboard=True
)

education_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Oliy"), KeyboardButton(text="Magistratura")],
        [KeyboardButton(text="Talaba"), KeyboardButton(text="O'rta maxsus")],
        [KeyboardButton(text="O'rta")],
        [KeyboardButton(text="Orqaga ↩️")]
    ], resize_keyboard=True, one_time_keyboard=True
)

education_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Высшее"), KeyboardButton(text="Магистратура")],
        [KeyboardButton(text="Студент"), KeyboardButton(text="Среднее специальное")],
        [KeyboardButton(text="Среднее")],
        [KeyboardButton(text="Назад ↩️")]
    ], resize_keyboard=True, one_time_keyboard=True
)

place_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Andijon'),
         KeyboardButton(text='Toshkent')],
        [KeyboardButton(text='Qashqadaryo'),
         KeyboardButton(text='Buhoro')],
        [KeyboardButton(text='Xiva'),
         KeyboardButton(text='Jizzax')],
        [KeyboardButton(text='Samarqand'),
         KeyboardButton(text="Farg'ona")],
        [KeyboardButton(text='Namangan'),
         KeyboardButton(text='Surxondaryo')],
        [KeyboardButton(text='Navoi'),
         KeyboardButton(text='Xorazm')]
    ], one_time_keyboard=False,
    resize_keyboard=True,
)

place_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Андижан'),
         KeyboardButton(text='Ташкент')],
        [KeyboardButton(text='Кашкадарья'),
         KeyboardButton(text='Бухара')],
        [KeyboardButton(text='Хива'),
         KeyboardButton(text='Джизак')],
        [KeyboardButton(text='Самарканд'),
         KeyboardButton(text="Фергана")],
        [KeyboardButton(text='Наманган'),
         KeyboardButton(text='Сурхандарья')],
        [KeyboardButton(text='Навои'),
         KeyboardButton(text='Хорезм')]
    ], one_time_keyboard=False,
    resize_keyboard=True,
)

program_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Word"), KeyboardButton(text="Excel"), KeyboardButton(text='Powerpoint')],
        [KeyboardButton(text="Orqaga ↩️")]
    ], resize_keyboard=True,
    one_time_keyboard=True
)

program_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Word"), KeyboardButton(text="Excel"), KeyboardButton(text='Powerpoint')],
        [KeyboardButton(text="Назад ↩️")]
    ], resize_keyboard=True,
    one_time_keyboard=True
)

family_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Turmush qurgan"), KeyboardButton(text='Turmush qurmagan')],
        [KeyboardButton(text="Ajrashgan")],
        [KeyboardButton(text="Orqaga ↩️")],
    ], resize_keyboard=True,
    one_time_keyboard=True
)

family_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Женат/Замужем"), KeyboardButton(text='Холост/Не замужем')],
        [KeyboardButton(text="Разведен")],
        [KeyboardButton(text="Назад ↩️")],
    ], resize_keyboard=True,
    one_time_keyboard=True
)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class SMS(StatesGroup):
    message = State()
    tg_id = State()


# Define States
class REG(StatesGroup):
    tg_id = State()
    number2 = State()
    education_level = State()
    place2 = State()
    edu_name = State()
    name = State()
    last_name = State()
    age = State()
    number = State()
    place = State()
    gender = State()
    is_student = State()
    education = State()
    family = State()
    last_work1 = State()
    last_work2 = State()
    last_work3 = State()
    language = State()
    audio = State()
    skills = State()
    used_program = State()
    photo = State()
    about_bot = State()


class Leng(Base):
    __tablename__ = 'leng'

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)
    user_language = Column(String, index=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_db())


def sanitize_value(value):
    if isinstance(value, (int, float, str)) or value is None:
        return value
    else:
        return str(value)  # Convert unsupported types to string


def create_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tg_id INTEGER,
                        place2 TEXT,
                        edu_name TEXT,
                        name TEXT,
                        last_name TEXT,
                        age INTEGER,
                        number TEXT,
                        number2 INTEGER,
                        place TEXT,
                        gender TEXT,
                        is_student TEXT,
                        education TEXT,
                        family TEXT,
                        last_work1 TEXT,
                        last_work2 TEXT,
                        last_work3 TEXT,
                        language TEXT,
                        audio TEXT,
                        skills TEXT,
                        used_program TEXT,
                        photo TEXT,
                        about_bot TEXT
                    )''')
    conn.commit()
    conn.close()

create_db()


async def set_user_language(tg_id: int, language: str):
    async with async_session() as session:
        stmt = select(Leng).where(Leng.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            user.user_language = language
        else:
            new_user = Leng(tg_id=tg_id, user_language=language)
            session.add(new_user)

        await session.commit()


async def get_user_language(tg_id: int) -> str:
    async with async_session() as session:
        stmt = select(Leng.user_language).where(Leng.tg_id == tg_id)
        result = await session.execute(stmt)
        user_language = result.scalar_one_or_none()
        return user_language


# Handlers
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Tilni tanglang / Выберите язык", reply_markup=language_keyboard)
    await state.set_state(REG.language)


@dp.message(lambda message: message.text in ["🇺🇿 Uz", "🇷🇺 Ru"])
async def select_language(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    language = 'uz' if message.text == "🇺🇿 Uz" else 'ru'

    if language == 'ru':
        await message.answer("Добро пожаловать в бот", reply_markup=register_ru)
    else:
        await message.answer("Botga xush kelibsiz", reply_markup=register_uz)
    await state.update_data(language=language)
    await set_user_language(tg_id, language)


@dp.message(F.text == "Anketa to'ldirish 📝")
async def anketa_uz(message: types.Message, state: FSMContext):
    await message.answer("👤 Ismingizni yozing:", reply_markup=back_uz)
    await state.set_state(REG.name)


@dp.message(F.text == "Заполнить анкету 📝")
async def anketa_ru(message: types.Message, state: FSMContext):
    await message.answer("👤 Введите ваше имя:", reply_markup=back_ru)
    await state.set_state(REG.name)


@dp.message(REG.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_language = await get_user_language(message.from_user.id)
    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        if user_language == "ru":
            await message.answer("Регистрация", reply_markup=register_ru)
        else:
            await message.answer("Registratsiyadan o'tish uchun pastdagi tugmani bosing", reply_markup=register_uz)
        return

    if user_language == "uz":
        await message.answer("👤 Familiyangizni yozing:", reply_markup=back_uz)
    else:
        await message.answer("👤 Введите вашу фамилию:", reply_markup=back_ru)
    await state.set_state(REG.last_name)


@dp.message(REG.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    user_language = await get_user_language(message.from_user.id)
    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.name)
        if user_language == "ru":
            await message.answer("Как вас зовут?")
        else:
            await message.answer("Ismingizni kiriting")
        return
    if user_language == "uz":
        await message.answer("Tug'ilgan sanangizni kiriting 🗓\nMisol uchun: 25.12.2008", reply_markup=back_uz)
    else:
        await message.answer("Введите вашу дату рождения 🗓\nПример: 25.12.2008", reply_markup=back_ru)
    await state.set_state(REG.age)


@dp.message(REG.age)
async def process_age(message: types.Message, state: FSMContext):
    age_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    user_language = await get_user_language(message.from_user.id)
    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.last_name)
        if user_language == "ru":
            await message.answer("👤 Введите вашу фамилию:", reply_markup=back_ru)
        else:
            await message.answer("👤 Familiyangizni yozing:", reply_markup=back_uz)
        return

    if not re.match(age_pattern, message.text):
        if user_language == "uz":
            await message.answer("Iltimos, tug'ilgan sanangizni 12.12.1900 formatda kiriting", reply_markup=back_uz)
        else:
            await message.answer("Пожалуйста, введите дату рождения в формате 12.12.1900", reply_markup=back_ru)
        return
    await state.update_data(age=message.text)
    if user_language == "uz":
        await message.answer("Telefon raqamingizni 998XXXXXXXXX formatda kiriting\n📞 Misol uchun: 998 99 999 99 99",
                             reply_markup=back_uz)
    else:
        await message.answer("Введите номер телефона в формате 998XXXXXXXXX\n📞 eg: 998 99 999 99 99",
                             reply_markup=back_ru)
    await state.set_state(REG.number)



@dp.message(REG.number2)
async def contact(message: types.Message, state: FSMContext):
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.number)
        if user_language == "ru":
            await message.answer("Введите номер телефона в формате 998XXXXXXXXX")
        else:
            await message.answer("Telefon raqamingizni 998 XX XXX XX XX formatida kiriting", reply_markup=back_uz)
        return

    if not message.contact:
        if user_language == 'uz':
            await message.answer("Telefon raqamni jo'natish uchun (Telefon raqamni ulashish) tugmasi ustiga bosing",
                                 reply_markup=contact_keyboard_uz)
        else:
            await message.answer('Для отправки номера телефона нажмите кнопку (Поделиться номером телефона)',
                                 reply_markup=contact_keyboard_ru)
        return

    number = message.contact.phone_number
    await state.update_data(number2=number)

    if user_language == "uz":
        await message.answer("🌐 Yashash manzilingiz viloyat(xaqiqiy turar joy):", reply_markup=place_uz)
    else:
        await message.answer("🌐 Введите ваш регион проживания:", reply_markup=place_ru)

    await state.set_state(REG.place)



def is_valid_phone_number(phone_number):
    pattern = re.compile(r"^\d{12}$")
    return pattern.match(phone_number) is not None


@dp.message(REG.number)
async def process_number(message: types.Message, state: FSMContext):
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.age)
        if user_language == "ru":
            await message.answer("Введите вашу дату рождения 🗓\nПример: 25.12.2008", reply_markup=back_ru)
        else:
            await message.answer("Tug'ilgan sanangizni kiriting 🗓\nMisol uchun: 25.12.2008", reply_markup=back_uz)
        return

    if not message.text or not is_valid_phone_number(message.text):
        if user_language == "uz":
            await message.answer("Iltimos, telefon raqamingizni 998XXXXXXXXX formatda kiriting")
        else:
            await message.answer("Пожалуйста, введите номер телефона в формате 998XXXXXXXXX")
        return

    await state.update_data(number=message.text)

    if user_language == "uz":
        await message.answer("Telefon raqamingizni yuborish uchun pastdagi tugmani bosing",
                             reply_markup=contact_keyboard_uz)
    else:
        await message.answer("Для отправки номера телефона нажмите кнопку (Поделиться номером телефона)",
                             reply_markup=contact_keyboard_ru)
    await state.set_state(REG.number2)


@dp.message(REG.place)
async def process_place(message: types.Message, state: FSMContext):
    await state.update_data(place=message.text)
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.number)
        if user_language == "ru":
            await message.answer("🌐 Введите ваш регион проживания:", reply_markup=place_ru)
        else:
            await message.answer("🌐 Yashash manzilingiz viloyat(xaqiqiy turar joy):", reply_markup=place_uz)
        return

    valid_places = [
        'Андижан', 'Ташкент', 'Кашкадарья', 'Бухара', 'Хива', 'Джизак', 'Самарканд', 'Фергана',
        'Наманган', 'Сурхандарья', 'Навои', 'Хорезм', 'Andijon', 'Toshkent', 'Qashqadaryo', 'Buhoro',
        'Xiva', 'Jizzax', 'Samarqand', "Farg'ona", 'Namangan', 'Surxondaryo', 'Navoi', 'Xorazm'
    ]

    if message.text not in valid_places:
        if user_language == "uz":
            await message.answer("Iltimos, tugmalardan birini tanlang", reply_markup=place_uz)
        else:
            await message.answer("Пожалуйста, выберите один из вариантов", reply_markup=place_ru)
        return

    if user_language == "uz":
        await message.answer("🧑👩 Jinsingizni tanlang:", reply_markup=gender_uz)
    else:
        await message.answer("🧑👩 Выберите ваш пол:", reply_markup=gender_ru)

    await state.set_state(REG.gender)


@dp.message(REG.gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.place)
        if user_language == "ru":
            await message.answer("🌐 Введите ваш регион проживания:", reply_markup=place_ru)
        else:
            await message.answer("🌐 Yashash manzilingiz viloyat(xaqiqiy turar joy):", reply_markup=place_uz)
        return

    if message.text not in ["👨 Erkak️", "👩‍🦰 Ayol", "👨 Мужчина️", "👩‍🦰 Женщина"]:
        if user_language == "uz":
            await message.answer("Iltimos, tugmalardan birini tanlang", reply_markup=gender_uz)
        else:
            await message.answer("Пожалуйста, выберите один из вариантов", reply_markup=gender_ru)
        return

    if user_language == "uz":
        await message.answer("Siz hozirda qaysidir universitet, litsey yoki kollej talabasimisiz?", reply_markup=yes_uz)
    else:
        await message.answer("Вы в настоящее время студент университета, лицея или колледжа?", reply_markup=yes_ru)
    await state.set_state(REG.is_student)


@dp.message(REG.is_student)
async def process_is_student(message: types.Message, state: FSMContext):
    await state.update_data(is_student=message.text)
    user_language = await get_user_language(message.from_user.id)
    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.gender)
        if user_language == "ru":
            await message.answer("🧑👩 Выберите ваш пол:", reply_markup=gender_ru)
        else:
            await message.answer("🧑👩 Jinsingizni tanlang:", reply_markup=gender_uz)
        return

    if message.text not in ['Ha', 'Yo\'q', 'Да', 'Нет']:
        if user_language == "uz":
            await message.answer("Iltimos, tugmalardan birini tanlang", reply_markup=yes_uz)
        else:
            await message.answer("Пожалуйста, выберите один из вариантов", reply_markup=yes_ru)
        return

    if user_language == "uz":
        await message.answer("💼 Maʼlumotingizni tanlang:", reply_markup=education_uz)
    else:
        await message.answer("💼 Выберите ваш уровень образования:", reply_markup=education_ru)
    await state.set_state(REG.education_level)


@dp.message(REG.education_level)
async def process_education_level(message: types.Message, state: FSMContext):
    await state.update_data(education_level=message.text)
    user_language = await get_user_language(message.from_user.id)
    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.is_student)
        if user_language == "ru":
            await message.answer("Вы в настоящее время студент университета, лицея или колледжа?", reply_markup=yes_ru)
        else:
            await message.answer("Siz hozirda qaysidir universitet, litsey yoki kollej talabasimisiz?",
                                 reply_markup=yes_uz)
        return

    valid_education_levels = ['Oliy', 'Magistratura', 'Talaba', 'O\'rta maxsus', 'O\'rta', 'Высшее', 'Магистратура',
                              'Студент', 'Среднее специальное', 'Среднее']
    if message.text not in valid_education_levels:
        if user_language == "uz":
            await message.answer("Iltimos, darajangizni tanglang", reply_markup=education_uz)
        else:
            await message.answer("Пожалуйста, выберите один из вариантов", reply_markup=education_ru)
        return

    if user_language == "uz":
        await message.answer("Ta‘lim muassasasining nomi va bitirgan yilingiz:", reply_markup=skip_uz)
    else:
        await message.answer("Введите название учебного заведения и год окончания:", reply_markup=skip_ru)
    await state.set_state(REG.education)


@dp.message(REG.education)
async def process_education(message: types.Message, state: FSMContext):
    await state.update_data(education=message.text)
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.education_level)
        if user_language == "ru":
            await message.answer("💼 Выберите ваш уровень образования:", reply_markup=education_ru)
        else:
            await message.answer("💼 Maʼlumotingizni tanlang:", reply_markup=education_uz)
        return

    if message.text == '▶️ O‘tkazib yuborish' or message.text == '▶️ Пропустить':
        if user_language == "ru":
            await message.answer("👨‍👩‍👧‍👦 Ваше семейное положение:", reply_markup=family_ru)
        else:
            await message.answer("👨‍👩‍👧‍👦 Oilaviy ahvolingiz:", reply_markup=family_uz)
        await state.set_state(REG.family)
        return

    if user_language == "uz":
        await message.answer("👨‍👩‍👧‍👦 Oilaviy ahvolingiz:", reply_markup=family_uz)
    else:
        await message.answer("👨‍👩‍👧‍👦 Ваше семейное положение:", reply_markup=family_ru)
    await state.set_state(REG.family)


@dp.message(REG.family)
async def process_family(message: types.Message, state: FSMContext):
    await state.update_data(family=message.text)
    user_language = await get_user_language(message.from_user.id)
    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.clear()
        await state.set_state(REG.education)
        if user_language == "ru":
            await message.answer("Введите название учебного заведения и год окончания:", reply_markup=skip_ru)
        else:
            await message.answer("Ta‘lim muassasasining nomi va bitirgan yilingiz:", reply_markup=skip_uz)
        return

    if message.text not in ["Женат/Замужем", "Холост/Не замужем", "Разведен", "Turmush qurgan", "Turmush qurmagan",
                            "Ajrashgan"]:
        if user_language == "uz":
            await message.answer("Iltimos, tugmalardan birini tanlang", reply_markup=family_uz)
        else:
            await message.answer("Пожалуйста, выберите один из вариантов", reply_markup=family_ru)
        return

    if user_language == "uz":
        await message.answer('👨‍🔧 Mutaxassisligingiz:', reply_markup=back_uz)
    else:
        await message.answer('👨‍🔧 Ваша специальность:', reply_markup=back_ru)
    await state.set_state(REG.last_work1)


@dp.message(REG.last_work1)
async def process_last_work1(message: types.Message, state: FSMContext):
    await state.update_data(last_work1=message.text)
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.set_state(REG.family)
        if user_language == "ru":
            await message.answer("👨‍👩‍👧‍👦 Ваше семейное положение:", reply_markup=family_ru)
        else:
            await message.answer("👨‍👩‍👧‍👦 Oilaviy ahvolingiz:", reply_markup=family_uz)
        return

    if user_language == "uz":
        await message.answer('Iltimos, o\'zingiz haqingizda bizga ovozli habar jo\'nating')
    else:
        await message.answer('Пожалуйста, отправьте нам голосовое сообщение о себе')
    await state.set_state(REG.audio)


@dp.message(REG.audio)
async def process_audio(message: types.Message, state: FSMContext):
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.set_state(REG.last_work1)
        if user_language == "ru":
            await message.answer('👨‍🔧 Ваша специальность:', reply_markup=back_ru)
        else:
            await message.answer('👨‍🔧 Mutaxassisligingiz:', reply_markup=back_uz)
        return

    if not message.voice:
        if user_language == "uz":
            await message.answer('🔊 Iltimos ovozli habar yuboring:')
        else:
            await message.answer('🔊 Пожалуйста, отправьте голосовое сообщение:')
        return

    print(f"Received message type: {'audio' if message.audio else 'voice' if message.voice else 'unknown'}")

    await state.update_data(audio=message.voice.file_id if message.voice else message.audio.file_id)
    user_language = await get_user_language(message.from_user.id)

    if user_language == "uz":
        await message.answer("Yaxshi qobiliyatlaringiz:")
    else:
        await message.answer("Ваши навыки:")
    await state.set_state(REG.skills)


@dp.message(REG.skills)
async def process_skills(message: types.Message, state: FSMContext):
    await state.update_data(skills=message.text)
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.set_state(REG.audio)
        if user_language == "ru":
            await message.answer("Пожалуйста, отправьте нам голосовое сообщение о себе", reply_markup=back_ru)
        else:
            await message.answer("Iltimos, o'zingiz haqingizda bizga ovozli habar jo'nating", reply_markup=back_uz)
        return

    if user_language == "uz":
        await message.answer("👨‍💻 Qaysi dasturlardan foydalana olasiz?", reply_markup=program_uz)
    else:
        await message.answer("👨‍💻 Какими программами вы владеете?", reply_markup=program_ru)
    await state.set_state(REG.used_program)


@dp.message(REG.used_program)
async def process_used_program(message: types.Message, state: FSMContext):
    await state.update_data(used_program=message.text)
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.set_state(REG.skills)
        if user_language == "ru":
            await message.answer("Ваши навыки:", reply_markup=back_ru)
        else:
            await message.answer("Yaxshi qobiliyatlaringiz:", reply_markup=back_uz)
        return

    if message.text not in ["Word", "Excel", "Powerpoint"]:
        if user_language == 'uz':
            await message.answer('Iltimos tugmalardan birini tanlang', reply_markup=program_uz)
        if user_language == 'ru':
            await message.answer('Пожалуйста, выберите один из вариантов', reply_markup=program_ru)
        return

    if user_language == "uz":
        await message.answer("Iltimos, surat yuboring", reply_markup=back_uz)
    else:
        await message.answer("Пожалуйста, отправьте фотографию", reply_markup=back_ru)
    await state.set_state(REG.photo)


@dp.message(REG.photo)
async def process_photo(message: types.Message, state: FSMContext):
    user_language = await get_user_language(message.from_user.id)

    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.set_state(REG.used_program)
        if user_language == "ru":
            await message.answer("👨‍💻 Какими программами вы владеете?", reply_markup=program_ru)
        else:
            await message.answer("👨‍💻 Qaysi dasturlardan foydalana olasiz?", reply_markup=program_uz)
        return

    if not message.photo:
        if user_language == "uz":
            await message.answer('🖼 Iltimos botga o\'z rasmingizni yuboring:', reply_markup=back_uz)
        else:
            await message.answer('🖼 Пожалуйста, отправьте своё фото:', reply_markup=back_ru)
        return

    await state.update_data(photo=message.photo[-1].file_id)

    if user_language == "uz":
        await message.answer("Biznning bot haqida fikirngiz", reply_markup=skip_uz)
    else:
        await message.answer("Где вы узнали о нашем боте?", reply_markup=skip_ru)
    await state.set_state(REG.about_bot)

    await state.set_state(REG.tg_id)

@dp.message(REG.tg_id)
async def tgid(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    await state.update_data(tg_id=tg_id)
    user_language = await get_user_language(message.from_user.id)

    if user_language == "uz":
        await message.answer("Bizning bot haqida qayerdan eshitdingiz?", reply_markup=back_uz)
    else:
        await message.answer("Где вы узнали о нашем боте?", reply_markup=back_ru)
    await state.set_state(REG.about_bot)


@dp.message(REG.about_bot)
async def process_about_bot(message: types.Message, state: FSMContext):
    await state.update_data(about_bot=message.text)
    user_language = await get_user_language(message.from_user.id)

    if message.text == 'Qaytatan':
        await state.set_state(REG.name)
        if user_language == "ru":
            await message.answer("👤 Введите ваше имя:", reply_markup=back_ru)
        else:
            await message.answer("👤 Ismingizni yozing", reply_markup=back_uz)
        return



    if message.text in ['Orqaga ↩️', 'Назад ↩️']:
        await state.set_state(REG.photo)
        if user_language == "ru":
            await message.answer("Пожалуйста, отправьте фотографию", reply_markup=back_ru)
        else:
            await message.answer("Iltimos, surat yuboring", reply_markup=back_uz)
        return


    if message.text in ['✅ Tastiqlayman', '✅ Я подтверждаю']:
        if user_language == "uz":
            await message.answer("Ro'yxatdan o'tish tugadi. Rahmat!")
        else:
            await message.answer("Регистрация завершена. Спасибо!")
        return
    user_data = await state.get_data()
    if user_language == "uz":
        await message.answer(
            f"Ismingiz: {user_data.get('name')}\nFamiliyangiz: {user_data.get('last_name')}\nTug'ilgan yilingiz: {user_data.get('age')}\nYashash manzilingiz: {user_data.get('place')}\nJinsingiz: {user_data.get('gender')}\nStudent: {user_data.get('is_student')}\nDarajangiz: {user_data.get('education_level')}\nBiladigan tillaringiz: {user_data.get('language')},\nTelefon raqamingiz {user_data.get('number')}{user_data.get('number2')}",
            reply_markup=confirm_uz)
    else:
        await message.answer(
            f"Ваше имя: {user_data.get('name')}\nВаша фамилия: {user_data.get('last_name')}\nВаш год рождения: {user_data.get('age')}\nВаш адрес проживания: {user_data.get('place')}\nВаш пол: {user_data.get('gender')}\nСтудент: {user_data.get('is_student')}\nВаш уровень образования: {user_data.get('education_level')}\nВаши языки: {user_data.get('language')}\nВаш номер телефона: {user_data.get('number', 'number2')}",
            reply_markup=confirm_ru)


    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO users (tg_id,place2, edu_name, name, last_name, age, number, number2, place, gender, is_student, education, family, last_work1, last_work2, last_work3, language, audio, skills, used_program, photo, about_bot)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (user_data.get('tg_id'),
                    user_data.get('place2'),
                    user_data.get('edu_name'),
                    user_data.get('name'),
                    user_data.get('last_name'),
                    user_data.get('age'),
                    user_data.get('number'),
                    user_data.get('number2'),
                    user_data.get('place'),
                    user_data.get('gender'),
                    user_data.get('is_student'),
                    user_data.get('education_level'),
                    user_data.get('family'),
                    user_data.get('last_work1'),
                    user_data.get('last_work2'),
                    user_data.get('last_work3'),
                    user_data.get('language'),
                    user_data.get('audio'),
                    user_data.get('skills'),
                    user_data.get('used_program')
                    , user_data.get('photo'),
                    user_data.get('about_bot')))

    conn.commit()
    conn.close()


async def main():
    await dp.start_polling(bot)


class TestMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        print("pass")
        result = await handler(event, data)
        print("pass 2")
        return result


print('working')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
