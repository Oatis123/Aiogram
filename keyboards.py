from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Inline():
    
    @staticmethod
    def menu():
        markup = InlineKeyboardMarkup()
        markup.add(*[InlineKeyboardButton(text='Сделать заказ✅', callback_data='order'), 
                    InlineKeyboardButton(text='О нас ❓', callback_data='about_us')])
        return markup
    
    @staticmethod
    def sus():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='sus', callback_data='suus'))
        return markup
    
    @staticmethod
    def order():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Ввести☑', callback_data='inpp'))
        return markup

    @staticmethod
    def back():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Вернуться в меню ⬅', callback_data='menu'))
        return markup
    
    @staticmethod
    def about_us():
        markup = InlineKeyboardMarkup()
        markup.add(*[InlineKeyboardButton(text='Нащи проекты🎴', callback_data='our'), 
                    InlineKeyboardButton(text='Вернуться в меню⬅', callback_data='menu')])
        return markup