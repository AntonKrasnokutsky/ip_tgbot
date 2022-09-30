import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bd.db import update_address_tvsp, update_net_tvsp
from bd.db import create_bd, create_tvsp, select_all_tvsp, select_tvsp


BOT_TOKEN = os.environ['TOKEN']
tvsp_new = False
tvsp_edit_addr = False
tvsp_edit_net = False
tvsp_edit_prefix = False
tvsp_edit_gateway = False
tvsp_edit_dns = False
tvsp_id = None
bot = telebot.TeleBot(BOT_TOKEN)


def gen_main_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("ТВСП", callback_data="tvsp"),
        InlineKeyboardButton("IP", callback_data="ip")
    )
    return markup


def gen_tvsp_markup(tvsps):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    btn = []
    for tvsp in tvsps:
        callback_data = "tvsp_view_" + str(tvsp[0])
        btn.append(InlineKeyboardButton(tvsp[1], callback_data=callback_data))
    btn.append(InlineKeyboardButton("Добавить", callback_data="tvsp_add"))
    btn.append(InlineKeyboardButton("Изменить", callback_data="tvsp_change"))
    btn.append(InlineKeyboardButton("Удалить", callback_data="tvsp_remove"))
    markup.add(*btn)
    return markup


def gen_tvsp_change(tvsps):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    btn = []
    for mark in tvsps:
        callback_data = 'tvsp_id_' + str(mark[0])
        btn.append(InlineKeyboardButton(mark[1], callback_data=callback_data))
    markup.add(*btn)
    return markup


def gen_tvsp_edit(tvsp_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    callback_data_addr = "tvsp_edit_addr_" + tvsp_id
    callback_data_net = "tvsp_edit_net_" + tvsp_id
    callback_data_prefix = "tvsp_edit_prefix_" + tvsp_id
    callback_data_gateway = "tvsp_edit_gateway_" + tvsp_id
    callback_data_dns = "tvsp_edit_dns_" + tvsp_id
    markup.add(
        InlineKeyboardButton("Адрес", callback_data=callback_data_addr),
        InlineKeyboardButton("Сеть", callback_data=callback_data_net),
        InlineKeyboardButton("Маска", callback_data=callback_data_prefix),
        InlineKeyboardButton("Шлюз", callback_data=callback_data_gateway),
        InlineKeyboardButton("DNS", callback_data=callback_data_dns)
    )
    return markup


def gen_ip_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Выдать", callback_data="ip_set"),
        InlineKeyboardButton("Освободить", callback_data="ip_clear")
    )
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global tvsp_new
    global tvsp_edit_addr
    global tvsp_edit_net
    global tvsp_edit_prefix
    global tvsp_edit_gateway
    global tvsp_edit_dns
    global tvsp_id

    if call.data == "tvsp":
        tvsp = select_all_tvsp()
        bot.send_message(
            call.from_user.id,
            'Подразделения',
            reply_markup=gen_tvsp_markup(tvsp)
        )
    elif call.data == "tvsp_add":
        tvsp_new = True
        bot.send_message(
            call.from_user.id,
            'Введи навание подразделения'
        )
    elif call.data == "tvsp_change":
        tvsp = select_all_tvsp()
        bot.send_message(
            call.from_user.id,
            'Выбери подраздление',
            reply_markup=gen_tvsp_change(tvsp)
        )
    elif 'tvsp_id_' in call.data:
        select_id = 8
        bot.send_message(
            call.from_user.id,
            'Выбери подраздление',
            reply_markup=gen_tvsp_edit(call.data[select_id:])
        )
    elif 'tvsp_view_' in call.data:
        len_pref = 10
        tvsp = select_tvsp(int(call.data[len_pref:]))
        message = ''
        for info in tvsp:
            message = 'Навзание: ' + info[1] + '\n'
            if info[2]:
                message += 'Адрес: ' + info[2] + '\n'
            if info[3]:
                message += 'Сеть: ' + info[3] + '\n'
            if info[4]:
                message += 'Маска: ' + info[4] + '\n'
            if info[5]:
                message += 'Шлюз: ' + info[5] + '\n'
            if info[6]:
                message += 'DNS: ' + info[6]
        bot.send_message(
            call.from_user.id,
            message
        )
    elif 'tvsp_edit_addr_' in call.data:
        tvsp_edit_addr = True
        len_pref = 15
        tvsp_id = int(call.data[len_pref:])
        bot.send_message(
            call.from_user.id,
            'Введи адрес подразделения'
        )
    elif 'tvsp_edit_net_' in call.data:
        tvsp_edit_net = True
        len_pref = 14
        tvsp_id = int(call.data[len_pref:])
        message = 'Введи сеть подразделения\n'
        message += 'Например 192.168.0.0'
        bot.send_message(
            call.from_user.id,
            message
        )
    elif 'tvsp_edit_prefix_' in call.data:
        tvsp_edit_prefix = True
        len_pref = 17
        tvsp_id = int(call.data[len_pref:])
        pass
    elif 'tvsp_edit_gateway_' in call.data:
        tvsp_edit_gateway = True
        len_pref = 18
        tvsp_id = int(call.data[len_pref:])
        pass
    elif 'tvsp_edit_dns_' in call.data:
        tvsp_edit_dns = True
        len_pref = 14
        tvsp_id = int(call.data[len_pref:])
        pass
    elif call.data == "ip":
        bot.send_message(
            call.from_user.id,
            'IP',
            reply_markup=gen_ip_markup()
        )


def var_clean():
    global tvsp_new
    global tvsp_edit_addr
    global tvsp_edit_net
    global tvsp_edit_prefix
    global tvsp_edit_gateway
    global tvsp_edit_dns
    global tvsp_id
    tvsp_new = False
    tvsp_edit_addr = False
    tvsp_edit_net = False
    tvsp_edit_prefix = False
    tvsp_edit_gateway = False
    tvsp_edit_dns = False
    tvsp_id = None


@bot.message_handler(content_types=['text'])
def message_handler(message):
    global tvsp_new
    global tvsp_edit_addr
    global tvsp_edit_net
    global tvsp_edit_prefix
    global tvsp_edit_gateway
    global tvsp_edit_dns
    global tvsp_id

    if message.text.lower() == 'бот':
        var_clean()
        bot.send_message(
            message.chat.id,
            'Слушаю',
            reply_markup=gen_main_markup()
        )
    elif tvsp_new:
        create_tvsp(message.text)
        tvsp_new = False
    elif tvsp_edit_addr:
        update_address_tvsp(tvsp_id, message.text)
        tvsp_edit_addr = False
        tvsp_id = None
    elif tvsp_edit_net:
        update_net_tvsp(tvsp_id, message.text)
        tvsp_edit_net = False
        tvsp_id = None


if __name__ == '__main__':
    create_bd()
    bot.polling(non_stop=True)
