import telebot

from config import TOKEN
import random

bot = telebot.TeleBot(TOKEN)
action = ''

def compress(path):
    txt = ''
    count = 0
    if len(path) == 0:
        return ''

    if len(path) == 1:
        txt += '1' + path[0]
        return txt
 
    for i in range(len(path)):
        count += 1
        if (i + 1) == len(path) or path[i] != path[i + 1]:
             txt += str(count) + path[i]
             count = 0
    return txt

def decompress(path):
    
    if len(path) == 0:
        return ''

    txt = ''
    i = 0
    while i <= len(path) - 2:
        for j in range(0, int(path[i])):
            txt += path[i+1]
        i += 2
    return txt

def show_menu(chatId):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True) # Создали клавиатуру
    
    item1 = telebot.types.KeyboardButton('Кодировать') # Создали кнопки
    item2 = telebot.types.KeyboardButton('Декодировать')

    markup.add(item1, item2)

    bot.send_message(chatId,'Выберите нужный вам пункт меню: ', reply_markup=markup)

""""Команда Старт"""
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,'Добро пожаловать!')
    show_menu(message.chat.id)

@bot.message_handler(content_types=['text'])
def send_text(message):
    global action
    if message.text == 'Кодировать':
        action = 'compress'
        bot.send_message(message.chat.id,'Введите строку для кодирования')
    elif message.text == 'Декодировать':
        action = 'decompress'
        bot.send_message(message.chat.id, 'Введите строку для декодирования')
    else:
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        item1 = telebot.types.InlineKeyboardButton('Показать меню', callback_data='1')
        markup.add(item1)
            
        if action == 'compress':
            bot.send_message(message.chat.id, compress(message.text), reply_markup=markup)
        elif action == 'decompress':
            bot.send_message(message.chat.id, decompress(message.text), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Вы не указали действие')
            show_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    show_menu(call.message.chat.id)

# bot.register_next_step_handler()

bot.polling(none_stop=True)
    