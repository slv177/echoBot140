import config
import telebot
import sqlite3
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import json

bot = telebot.TeleBot(config.token)

def getAllRecords():
    # Creates SQLite database to store info.
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    print('2connected')
    answer = cur.execute('''SELECT * FROM info;''')
    print(answer)
    return [answer]

reply_keyboard = [['Name', 'Age'], ['Address', 'Amount'], ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

@bot.message_handler(commands='test')
def start(message):
    answer = getAllRecords()
    # keyboard = build_keyboard(answer)
    bot.send_message(message.chat.id, text=json.dumps(answer))

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

if __name__ == '__main__':
    bot.infinity_polling()