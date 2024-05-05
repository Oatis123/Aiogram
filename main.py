import sqlite3
import logging
import os
import re
import yaml
import phonenumbers
from keyboards import Inline as kb
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

logging.basicConfig(level=logging.INFO)

load_dotenv('secret.env')

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.setup_middleware(LoggingMiddleware())

class Texts:
    def __init__(self, file_path='texts.yaml'):
        with open(file_path, 'r', encoding='utf-8') as file:
            texts = yaml.safe_load(file)
            
            for key, value in texts.items():
                setattr(self, key, value)

text = Texts()

def valid_number(number: str):
    try:
        phone_number = phonenumbers.parse(number, None)
        return phonenumbers.is_valid_number(phone_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


@dp.message_handler(commands=["start"])
async def start_handler(message: Message):
    await message.answer(Texts().greet.format(name=message.from_user.full_name), reply_markup=kb.menu())


@dp.message_handler(commands=["amogus"])
async def amogus(message: Message):
    await message.answer(text.sus, reply_markup=kb.sus())


@dp.callback_query_handler(lambda callback: callback.data=='order')
async def order(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text.tp)
    await state.set_state('ordering')


@dp.message_handler(state='ordering')
async def save_info(message: Message, state: FSMContext):
    phone, name = message.text.rsplit(maxsplit=1)
    print(phone, name)

    if valid_number(phone):
        formatted_phone = re.sub(r"[^\d]", "", phone)
        if phone.startswith('+'): formatted_phone = '+' + formatted_phone
        with sqlite3.connect('client.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM clients WHERE phone = ?', (formatted_phone,))
            if cur.fetchone()[0]:
                await message.answer(text.tryy)
                return
            else:
                cur.execute('INSERT INTO clients (user_id, phone, name) VALUES (?, ?, ?)', (message.from_user.id, formatted_phone, name))

                await state.reset_state()

        
        await message.answer(text.ready, reply_markup=kb.back())

    else:
        await message.answer(text.tryy)
        


@dp.callback_query_handler(lambda callback: callback.data=='menu')
async def ready(callback: CallbackQuery):
    await callback.message.edit_text(text.grit, reply_markup=kb.menu())


@dp.callback_query_handler(lambda callback: callback.data=='about_us')
async def ready(callback: CallbackQuery):
    await callback.message.edit_text(text.us, reply_markup=kb.about_us())


@dp.callback_query_handler(lambda callback: callback.data=='our')
async def ready(callback: CallbackQuery):
    await callback.message.edit_text(text.our, reply_markup=kb.back())


@dp.message_handler(commands=["clients"])
async def base(message: Message):
    if str(message.from_user.id) in os.environ.get("admin_id").split(','):
        with sqlite3.connect('client.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT phone, name FROM clients')
            users_data = cur.fetchall()

            await message.answer('\n'.join(f'{phone} - {name}' for phone, name in users_data))

    else:
        await message.answer(text.d)


@dp.message_handler(commands=["clear"])
async def base(message: Message):
    if str(message.from_user.id) in os.environ.get("admin_id").split(','):
        with sqlite3.connect('client.db') as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM "clients"')
            cur.execute("DELETE FROM sqlite_sequence WHERE name='clients'")
            await message.answer(text.clear, reply_markup=kb.back())
    else:
        await message.answer(text.d)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    