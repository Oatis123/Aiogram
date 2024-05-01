from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


menu = [
    [InlineKeyboardButton(text='Сделать заказ✅', callback_data='order'), InlineKeyboardButton(text='О нас ❓', callback_data='about_us')]
]

sus = [[InlineKeyboardButton(text='sus', callback_data='suus')]]

order = [[InlineKeyboardButton(text='Ввести☑', callback_data='inpp')]]

back = [[InlineKeyboardButton(text='Вернуться в меню⬅', callback_data='menu')]]

about_us = [[InlineKeyboardButton(text='Нащи проекты🎴', callback_data='our')], 
             [InlineKeyboardButton(text='Вернуться в меню⬅', callback_data='menu')]]


about_us = InlineKeyboardMarkup(inline_keyboard=about_us)
back = InlineKeyboardMarkup(inline_keyboard=back)
order = InlineKeyboardMarkup(inline_keyboard=order)
sus = InlineKeyboardMarkup(inline_keyboard=sus)
menu = InlineKeyboardMarkup(inline_keyboard=menu)