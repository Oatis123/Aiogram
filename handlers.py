from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import kb
import text
from aiogram import flags
import admin
import csv

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(Command("amogus"))
async def messege_handler(msg: Message):
    await msg.answer(text.sus, reply_markup=kb.sus)


@router.callback_query(F.data == 'order')
async def order(clbck):
    await clbck.message.edit_text(text.tp)
    @router.message()
    async def save_info(msg: Message):
        a = 'абвгдеёжзийклмнопрстуфхшщцчъыьэюяАБВГДЕЁЖЗИЁКЛМНОПРСТУФШЩХЦЧЪЫЬЭЮЯ'
        if (msg.text[0] == '8' or msg.text[0] == 8 or msg.text[0] == '+') and msg.text[-1] in a:
            info = msg.text
            with open('client.csv', 'a', newline='', encoding='utf8') as f:
                fwriter = csv.writer(f)
                fwriter.writerow(info.split(' '))
                f.close()
            await msg.answer(text.ready, reply_markup=kb.back)
        else:
            await msg.answer(text.tryy)


@router.callback_query(F.data == 'menu')
async def ready(clbck):
    await clbck.message.edit_text(text.grit, reply_markup=kb.menu)


@router.callback_query(F.data == 'about_us')
async def ready(clbck):
    await clbck.message.edit_text(text.us, reply_markup=kb.back)
