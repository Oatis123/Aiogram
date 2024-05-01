import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import kb
import text
from aiogram import flags
import admin
import csv
import config


async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

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
    await clbck.message.edit_text(text.us, reply_markup=kb.about_us)


@router.callback_query(F.data == 'our')
async def ready(clbck):
    await clbck.message.edit_text(text.our, reply_markup=kb.back)


@router.message(Command('clients'))
async def base(msg: Message):
    if str(msg.from_user.id) == admin.admin_id:
        with open('client.csv', 'r', encoding='utf8') as f:
            fs = f.readlines()
            await msg.answer(''.join(fs))
            f.close()
    else:
        await msg.answer(text.d)


@router.message(Command('clear'))
async def base(msg: Message):
    if str(msg.from_user.id) == admin.admin_id:
        with open('client.csv', 'w', encoding='utf8') as f:
            fwriter = csv.writer(f)
            fwriter.writerow(' ')
            f.close()
            await msg.answer(text.clear, reply_markup=kb.back)
    else:
        await msg.answer(text.d)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    