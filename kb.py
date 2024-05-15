from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


menu = [
    [InlineKeyboardButton(text='Сделать заказ✅', callback_data='order'), InlineKeyboardButton(text='О нас ❓', callback_data='about_us')], [InlineKeyboardButton(text='Тестовое меню"{}"', callback_data='menu_plus')]]

sus = [[InlineKeyboardButton(text='sus', callback_data='suus')]]

order = [[InlineKeyboardButton(text='Ввести☑', callback_data='inpp')]]

back = [[InlineKeyboardButton(text='Вернуться в меню⬅', callback_data='menu')]]

back_p = [[InlineKeyboardButton(text='Вернуться в меню⬅', callback_data='menu'), InlineKeyboardButton(text='Подарок🎁', callback_data='present')]]

about_us = [[InlineKeyboardButton(text='Нащи проекты🎴', callback_data='our')], 
             [InlineKeyboardButton(text='Вернуться в меню⬅', callback_data='menu')]]


present = [[InlineKeyboardButton(text='Подписаться на канал➡', callback_data='folow')], [InlineKeyboardButton(text='Проверить подписку✔', callback_data='check')]]


menu_plus = [[InlineKeyboardButton(text='Робот "кумир" 📱', callback_data='robot'), InlineKeyboardButton(text='Вернуться в меню⬅', callback_data='menu')]]


clients = [[InlineKeyboardButton(text='Очистить', callback_data='clear'), InlineKeyboardButton(text='Просмотр', callback_data='see')]]


menu_back = [[InlineKeyboardButton(text='Вернуться в тестовое меню◀', callback_data='menu_plus')]]


back_admins = [[InlineKeyboardButton(text='Назад', callback_data='backa')]]

menu_back = InlineKeyboardMarkup(inline_keyboard=menu_back)
back_admins = InlineKeyboardMarkup(inline_keyboard=back_admins)
clients = InlineKeyboardMarkup(inline_keyboard=clients)
menu_plus = InlineKeyboardMarkup(inline_keyboard=menu_plus)
present = InlineKeyboardMarkup(inline_keyboard=present)
back_p = InlineKeyboardMarkup(inline_keyboard=back_p)
about_us = InlineKeyboardMarkup(inline_keyboard=about_us)
back = InlineKeyboardMarkup(inline_keyboard=back)
order = InlineKeyboardMarkup(inline_keyboard=order)
sus = InlineKeyboardMarkup(inline_keyboard=sus)
menu = InlineKeyboardMarkup(inline_keyboard=menu)