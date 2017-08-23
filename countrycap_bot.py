import sys
import os
import json
import codecs
import re
import asyncio
import random
import telepot.aio
# from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from time import strftime
import misc
import random


async def on_chat_message(msg):
    global answerData, lowerCountries

    content_type, chat_type, chat_id = telepot.glance(msg)
    chat_id_str = str(chat_id)

    # вписываем новый id в csv файл
    print(chat_id_str+' может быть добавлен в список id')
    #

    with open('countrycap.log', 'a', encoding='utf8') as logFile:
        if content_type != 'text':
            return

        logFile.write('['+strftime("%Y-%m-%d %H:%M:%S")+']['+chat_id_str+' -> bot]: '+msg['text']+'\n')
        print('Chat:', content_type, chat_type, chat_id)
        print('Пользователь '+chat_id_str+' написал:\n'+msg['text'].lower())
        request = msg['text']  # .lower()

        if request in ('/start', 'hi', 'help', 'привет', 'помоги мне', 'помощь', 'старт'):
            await bot.sendMessage(chat_id, answerData['welcome'])  # ,reply_markup=rkh)
            logFile.write('['+strftime("%Y-%m-%d %H:%M:%S")+'][bot -> '+chat_id_str+']: '+answerData['welcome']+'\n')
            return
        elif request in ("тест"):
            testAnswers = ["Скопье", 'Тирана', 'Мапуту', 'Подгорица']
            inline_keyboard = []
            for a in range(len(testAnswers)):
                inline_keyboard.append([InlineKeyboardButton(text=testAnswers[a], callback_data=testAnswers[a])])
            ikm = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await bot.sendMessage(chat_id, 'Выберете столицу Македонии:', reply_markup=ikm)
        elif request in answerData['countries'].keys():
            se = random.randint(0, 1)
            phraseNumber = random.randint(0, 4)
            if se == 0:
                add = answerData["addsToAnswer"]['start'][phraseNumber]
                await bot.sendMessage(chat_id, add+answerData['countries'][request])
                logFile.write(
                    '['+strftime("%Y-%m-%d %H:%M:%S")+'][bot -> '+chat_id_str+']: '+add+answerData['countries'][
                        request]+'\n')
            else:
                add = answerData["addsToAnswer"]['end'][phraseNumber]
                await bot.sendMessage(chat_id, answerData['countries'][request]+"."+add)
                logFile.write('['+strftime("%Y-%m-%d %H:%M:%S")+'][bot -> '+chat_id_str+']: '+answerData['countries'][
                    request]+add+'\n')
            return
        elif request in lowerCountries:
            await bot.sendMessage(chat_id, answerData["lowCountryRequest"])
            logFile.write(
                '['+strftime("%Y-%m-%d %H:%M:%S")+'][bot -> '+chat_id_str+']: '+answerData["lowCountryRequest"]+'\n')
            return
        elif request.lower() in ["хуй", "Хуй", "Ты хуй", "ты хуй"]:
            await bot.sendMessage(chat_id, "Сам ты ХУЙ!")
            logFile.write('['+strftime("%Y-%m-%d %H:%M:%S")+'][bot -> '+chat_id_str+']: '+"Сам ты ХУЙ!"+'\n')
            return
        elif request.lower() in ["пидор", "Пидор"]:
            await bot.sendMessage(chat_id,
                                  "Спорное утверждение, но одно я знаю точно, что пидор здесь один и это не я!")
            logFile.write('['+strftime(
                "%Y-%m-%d %H:%M:%S")+'][bot -> '+chat_id_str+']: '+"Спорное утверждение, но одно я знаю точно, что пидор здесь один и это не я!"+'\n')
            return
        else:
            await bot.sendMessage(chat_id, answerData['badRequest'])


async def on_callback_query(msg):
    global answerData
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)
    if query_data == answerData['countries']['Македония']:
        await bot.sendMessage(-229031523, "Верно!")
    else:
        await bot.sendMessage(-229031523, "Не тупи. Очень прошу)")


homeDir = os.path.dirname(__file__)
lowerCountries = []
# with open(os.path.join(homeDir, 'answersData.json'), encoding='utf8') as answerDataFile:
print('Loading meta...')
answerData = json.load(codecs.open('answersData.json', 'r', 'utf-8-sig'))
for country in answerData['countries'].keys():
    lowerCountries.append(country.lower())
# print(answerData['countries'].keys())
print('answers loaded!')

bot = telepot.aio.Bot(misc.token)

loop = asyncio.get_event_loop()
# для получения данных от inline выбора добавляем callback_query и указываем функцию, которая будет срабатывать при ответах.
loop.create_task(bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query}))
print('Listening ...')

loop.run_forever()
