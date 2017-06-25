# -*- coding: utf-8 -*-

import config
import telebot
import re
bot = telebot.TeleBot(config.token)


def calculation(network, mask):
    subnet = []
    broadcast = []
    broadstr1 = []
    hsmax = []

    a = [('1' * int(mask) + '0' * (32 - int(mask)))[i:
    i + 8] for i in range(0, len(('1' * int(mask) + '0' * (32 - int(mask)))), 8)]
    broadstr = ''

    for i in range(len((network.split('.')))):
        okt = int(network.split('.')[i]) & (int(a[i], 2))
        subnet.append(okt)
        broad = str(bin(okt))[2:].rjust(8, '0')
        broadcast.append(broad)
        broadstr += broad


    hostmin = subnet.copy()
    hostmin[3] += 1
    t = broadstr[:int(mask)] + '1' * (32 - int(mask))
    hostmax = broadstr[:int(mask)] + '1' * (32 - int(mask) - 1) + '0'



    for n in [t[i:i + 8] for i in range(0, len(t), 8)]:
        broadstr1.append(int(n, 2))
    for n in [hostmax[i:i + 8] for i in range(0, len(hostmax), 8)]:
        hsmax.append(int(n, 2))


    return ('.'.join(map(str, subnet)), '.'.join(map(str, broadstr1)), '.'.join(map(str, hostmin)), '.'.join(map(str, hsmax)))

@bot.message_handler(commands=["ip"])
def send_welcome(message):
    msg = bot.send_message(message.chat.id,
    'Вам необходимо знать IP-адрес и маску сети. '
    'Введите IP-адрес и маску сети в формате 123.123.123.123/15'
    )
    bot.register_next_step_handler(msg, get_data)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'Привет. '
    'Это бот, который помогает находить параметры сети. '
    )

@bot.message_handler(commands=["help"])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'Мои команды:\n'
    '/start - Приветственное сообщение\n'
    '/ip - Узнать параметры сети\n'
    '/help - Список команд'
    )



def get_data(message):
    if message.text in ('/help','/start','/ip'):
        return
    else:
        pattern = re.compile(
            "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\/.+$")
        if pattern.match(message.text) is None:
            msg = bot.send_message(message.chat.id,
                                   'Вы ввели неверный IP адрес. Попробуйте еще раз')
            bot.register_next_step_handler(msg, get_data)
        else:
            network = message.text.split('/')[0]
            mask = message.text.split('/')[1]
            if int(mask) in range(0,33):
                bot.send_message(message.chat.id, 'Адрес сети: {}\nШироковещательный адрес: {}\nHostmin: {}\nHostmax: {}'.format(*calculation(network, mask)))
                #bot.register_next_step_handler(message, get_data)
            else:
                msg = bot.send_message(message.chat.id, 'Введена некорректная маска. Попробуйте еще раз')
                bot.register_next_step_handler(msg, get_data)


if __name__ == '__main__':
    bot.polling(none_stop=True)