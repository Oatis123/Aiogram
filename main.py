import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import ContentType
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types, F, Router
from aiogram.types import Message, File, document
from aiogram.filters import Command
import kb
import text
from aiogram import flags
import csv
import secret
import os
import tkinter as tk
from tkinter import filedialog
import random



def encrypt_message(message, key):
    encrypted_message = ""
    for char in message:
        encrypted_message += chr(ord(char) + key)
    return encrypted_message


def decrypt_message(encrypted_message, key):
    decrypted_message = ""
    for char in encrypted_message:
        decrypted_message += chr(ord(char) - key)
    return decrypted_message


class Cell:
    def __init__(self, x, y, walls=0, color=False, point=False, finish=False, start=False) -> None:
        self.x = x
        self.y = y
        self.walls = walls
        self.color = color
        self.point = point
        self.finish = finish
        self.start = start
        self.visited = False
        

    def __repr__(self):
        if self.finish:
            return "Б"
        elif self.color:
            return "*"
        elif self.visited:
            return "?"

        elif self.point:
            return "+"
        elif self.start:
            return "А"

        else:
            return "·"


def parse_file(file):
    with open(file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    # Пропускаем комментарии и пустые строки
    lines = [line for line in lines if line.strip() and not line.startswith(';')]
    print(''.join(lines[2:]))
    
    field_size = tuple(map(int, lines[0].split()))
    
    field = [[Cell(x, y) for x in range(field_size[0])] for y in range(field_size[1])]
    # hashstr = '\n'.join([''.join(['#' for _ in range(field_size[0])]) for _ in range(field_size[1])])
    # print(hashstr)
    
    for line in lines[2:]:
        parts = line.split()
        x, y = map(int, parts[:2])
        walls = int(parts[2])
        point = parts[-1] == '1'
        finish = 'Б' in parts
        color = bool(int(parts[3]))
        field[y][x] = Cell(x, y, walls, color, point, finish)

    x, y = tuple(map(int, lines[1].split())) # start position
    cell = field[y][x]
    cell.start = True
    # print(field[y][x].start)

    # for y in range(len(field)):
    #     for x, cell in enumerate(field[y]):
    #         if cell==None:
    #             field[y][x] = Cell(x, y)
    
    return field


def has_wall(cell, direction):
    
    walls = {
        "left": [1, 3, 5, 7, 9, 11, 13, 15],
        "right": [2, 3, 6, 7, 10, 11, 14, 15],
        "up": [8, 9, 10, 11, 12, 13, 14, 15],
        "down": [4, 5, 6, 7, 12, 13, 14, 15],
    }
    return cell.walls in walls[direction]

def get_neighbors(cell, field):
    # print(cell)
    neighbors = {} # {neighbour: 'up'}
    rows = len(field)
    cols = len(field[0])
    
    directions = [('up', -1, 0, 'down'), ('down', 1, 0, 'up'), ('left', 0, -1, 'right'), ('right', 0, 1, 'left')]
    for direction, dy, dx, revdirection in directions:
        nx, ny = cell.x + dx, cell.y + dy
        # print(newcell.x, newcell.y)
        
        if 0 <= nx < cols and 0 <= ny < rows:
            newcell = field[ny][nx]
            if not has_wall(cell, direction) and not has_wall(newcell, revdirection):
                # print(cell.walls)

                neighbors[newcell] = direction
    
    return neighbors


def find_closest_cell(start, field, points=[], mode='point'):
    # if start.point:
    #     return start, [start]

    visited = set()
    queue = [(start, [], [start])] 

    while queue:
        current, directions, path = queue.pop(0) 
        visited.add((current.y, current.x))

        if (mode == 'point' and current in points) or (mode == 'finish' and current.finish):
            for cell in path[1:-1]: cell.visited =True
            return current, directions, path


        for neighbor, direction in get_neighbors(current, field).items():
            if ((neighbor.y, neighbor.x) not in visited): #or (cell.point and not cell.color)
                queue.append((neighbor, directions + [direction], path + [neighbor]))  
                visited.add((neighbor.y, neighbor.x))

        print(queue)
        print(visited)

    return None, [], []

def code_builder(commands):
    kumir = {
        'up' : 'вверх',
        'down' : 'вниз',
        'right' : 'вправо',
        'left' : 'влево',
        'paint' : 'закрасить',
    }
    code = [kumir[command] for command in commands]

    return '\n'.join(code)


def solver(field):
    

    for row in field:
        print(' '.join([str(cell) for cell in row]))
    print('\n')

    points_to_paint = [cell for row in field for cell in row if cell.point and not cell.color]
    print([cell for row in field for cell in row])
    current_cell = [cell for row in field for cell in row if cell.start][0]



    commands = []
    while points_to_paint:
        closest_point, directions, path = find_closest_cell(current_cell, field, points_to_paint, 'point')
        print(closest_point, directions, path)
        if closest_point is None:
            break

        closest_point.color = True
        points_to_paint = [cell for cell in points_to_paint if not cell.color]
        current_cell = closest_point
        commands += directions + ['paint']

        for row in field:
            print(' '.join([str(cell) for cell in row]))

        for row in field:
            for cell in row:
                cell.visited = False

    closest_point, directions, path = find_closest_cell(closest_point, field, mode='finish')
    print(closest_point, directions, path)
    commands += directions

    for row in field:
        print(' '.join([str(cell) for cell in row]))

    return commands


def solve(file):
    field = parse_file(file)
    return code_builder(solver(field))


async def main():
    bot = Bot(token=secret.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


bot = Bot(token=secret.BOT_TOKEN)
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
            await msg.answer(text.ready, reply_markup=kb.back_p)
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
    await msg.answer(text.clients, reply_markup=kb.clients)


@router.callback_query(F.data == 'backa')
async def base(clbck):
    await clbck.message.edit_text(text.clients, reply_markup=kb.clients)


@router.callback_query(F.data == 'see')
async def base(clbck):
    if str(clbck.from_user.id) in secret.admin_id:
            with open('client.csv', 'r', encoding='utf8') as f:
                fs = f.readlines()
                if fs != []:
                    await clbck.message.edit_text(''.join(fs), reply_markup=kb.back_admins)
                else:
                    await clbck.message.edit_text('Нет новых клиентов...', reply_markup=kb.back_admins)
                f.close()
    else:
            await clbck.message.answer(text.d)



@router.callback_query(F.data == 'clear')
async def base(clbck):
    if str(clbck.from_user.id) in secret.admin_id:
        f = open('client.csv', 'w')
        f.truncate()
        f.close()
        await clbck.message.edit_text(text.clear, reply_markup=kb.back_admins)
    else:
        await clbck.message.answer(text.d)


@router.callback_query(F.data == 'present')
async def present(clbck):
    await clbck.message.answer(text.present, reply_markup=kb.present)


@router.callback_query(F.data == 'menu_plus')
async def menu_plus(clbck):
    await clbck.message.edit_text(text.menu_plus, reply_markup=kb.menu_plus)



@router.callback_query(F.data == 'robot')
async def stert_sol(clbck):
    await clbck.message.edit_text('Отправьте фалй .fil с заданием:', reply_markup=kb.menu_back)
    @router.message(F.document)
    async def handle_docs_file(msg: Message):
        file_id = msg.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path

        file_name = f"{msg.document.file_name}"
        await bot.download_file(file_path, file_name)

        await msg.answer(solve(file_name), reply_markup=kb.menu_back)
        os.remove(file_name)


@router.callback_query(F.data == 'codec')
async def codec(clbck):
    await clbck.message.answer('Меню для шифровки и дешифровки сообщений', reply_markup=kb.code)


@router.callback_query(F.data == 'code')
async def code(clbck):
    await clbck.message.answer('Отправьте текст для шифровки:')
    @router.message()
    async def codes(msg: Message):
        text = msg.text
        k = random.choice(secret.keys)
        texte = encrypt_message(text, k)
        texte = f'Зашифрованое сообщение: {texte}' + f'\nЗапомните данный ключ для дешифровки: {k}'
        await msg.answer(texte, reply_markup=kb.menu_back)



@router.callback_query(F.data == 'uncode')
async def uncode(clbck):
    await clbck.message.answer('Отправьте текст и ключ для расшифровки через пробел в формате (текст ключ):')
    @router.message()
    async def codes(msg: Message):
        text = msg.text
        texte = text.split(' ')
        key = texte[-1]
        texte.pop(-1)
        texte = ' '.join(texte)
        await msg.answer(f'Расшифрованный текс: {decrypt_message(texte, key)}', reply_markup=kb.menu_back)
        




        
        

            





    



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    