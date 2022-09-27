import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bd.db import create_bd
BOT_TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Get IP", callback_data="get_ip"),
        InlineKeyboardButton("No", callback_data="cb_no")
    )
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call)
    print('')
    if call.data == "get_ip":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Кнопка", url="https://rgbfish.ru"))
        bot.send_message(call.from_user.id, 'Что-то происходит', reply_markup=markup)
        # bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    print(message.chat)
    print('')
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())


if __name__ == '__main__':
    create_bd()
    bot.polling(non_stop=True)
