from telebot import TeleBot
import config
import telebot
from collections import defaultdict
from telebot import types
import sqlite3

USER_REQUEST = defaultdict(lambda: {})

def update_request(user_id, key, value):
    USER_REQUEST[user_id][key] = value

def get_request(user_id):
    return USER_REQUEST[user_id]

bot: TeleBot = telebot.TeleBot(config.token)

root_menu_data = (("Купить","buy"),("Продать","sell"),("Услуги","service"))
buy_menu_data = (("Авто","auto"),("Недвижимость","realestate"),("Разное","misc"))
sell_menu_data = (("Авто","auto"),("Недвижимость","realestate"),("Питание","food"),("Разное","misc"))
service_menu_data = (("Авто","auto"),("Красота","beauty"),("Парикмахер","barber"),("Разное","misc"))


def show_keyboard_and_message(message, data_for_buttons, text_to_display):
    key = types.InlineKeyboardMarkup(row_width=2)
    for item in data_for_buttons:
        button = types.InlineKeyboardButton(text=str(item[0]), callback_data=str(item[1]))
        key.add(button)
    bot.send_message(message.chat.id, text_to_display, reply_markup=key)


@bot.message_handler(commands=["reset"])
def recet_user_data():
        update_request(c.message.chat.id, None, None)


@bot.message_handler(commands=["start"])
def inline(message):
    show_keyboard_and_message(message, root_menu_data, 'Выберите раздел объявлений')

@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    if str(c.data) == 'buy':
        update_request(c.message.chat.id, 'section', "buy")
        show_keyboard_and_message(c.message, buy_menu_data, "Выберите категорию")


    if str(c.data) == 'sell':
        update_request(c.message.chat.id, 'section', "sell")
        key = types.InlineKeyboardMarkup()
        show_keyboard_and_message(c.message, sell_menu_data, "Выберите категорию")

    if str(c.data) == 'service':
        update_request(c.message.chat.id, 'section', "service")
        key = types.InlineKeyboardMarkup()
        show_keyboard_and_message(c.message, service_menu_data, "Выберите категорию")

    if c.data == 'auto':
        update_request(c.message.chat.id, 'subsection', "auto")
        pubs = get_records(USER_REQUEST[c.message.chat.id]['section'], USER_REQUEST[c.message.chat.id]['subsection'])
        for item in pubs:
            bot.send_message(c.message.chat.id, item[0])

    if c.data == 'realestate':
        update_request(c.message.chat.id, 'subsection', "realestate")
        pubs = get_records(USER_REQUEST[c.message.chat.id]['section'], USER_REQUEST[c.message.chat.id]['subsection'])
        for item in pubs:
            bot.send_message(c.message.chat.id, item[0])

    if c.data == 'misc':
        update_request(c.message.chat.id, 'subsection', "misc")
        pubs = get_records(USER_REQUEST[c.message.chat.id]['section'], USER_REQUEST[c.message.chat.id]['subsection'])
        for item in pubs:
            bot.send_message(c.message.chat.id, item[0])

    if c.data == 'barber':
        update_request(c.message.chat.id, 'subsection', "barber")
        pubs = get_records(USER_REQUEST[c.message.chat.id]['section'], USER_REQUEST[c.message.chat.id]['subsection'])
        for item in pubs:
            bot.send_message(c.message.chat.id, item[0])

    if c.data == 'beauty':
        update_request(c.message.chat.id, 'subsection', "beauty")
        pubs = get_records(USER_REQUEST[c.message.chat.id]['section'], USER_REQUEST[c.message.chat.id]['subsection'])
        for item in pubs:
            bot.send_message(c.message.chat.id, item[0])


def get_records(section, subsection):
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    sqlite_getinfo_query = '''SELECT message FROM info WHERE section=? AND subsection=?;'''
    cursor.execute(sqlite_getinfo_query, (section, subsection))
    info_from_db = cursor.fetchall()
    return info_from_db

@bot.message_handler(commands=["top"])
def get_top_records(message):
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    sqlite_getinfo_query = '''SELECT message FROM info WHERE top=true;'''
    cursor.execute(sqlite_getinfo_query)
    info_from_db = cursor.fetchall()
    for item in info_from_db:
        bot.send_message(message.chat.id, item[0])


if __name__ == '__main__':
    bot.infinity_polling()

