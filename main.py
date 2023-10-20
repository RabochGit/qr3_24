import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State
import datetime
import random

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6484506724:AAHgDGcm9MrhTBQ9AUX9GLZzVpq2CHz21yg",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "новости"  # Можно менять текст
text_button_1 = "Интересный факт"  # Можно менять текст
text_button_2 = "Лучшая онлайн школа"  # Можно менять текст
text_button_summer = "Когда лето?"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_summer,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Что будем делать?',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id,
                     'Подборка самых интересных [новостей](https://dzen.ru/news?issue_tld=ru&utm_referrer=dzen.ru) за день')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def possibillityes(message):
    poss = ['Человек в течение жизни создаёт столько слюны, что ею можно заполнить два средних размеров бассейна.',
            'Мужчины в течение жизни тратят 3 350 часов на сбривание 8,4 метров щетины.',
            'Дети в возрасте от 1 до 3 месяцев плачут без слёз.',
            'Приблизительно 365 миллионов человек в мире имеют компьютеры, а половина населения земного шара никогда не видели и не использовали телефон.',
            'Домохозяйка в среднем проходит 11 километров в день, занимаясь домашними делами.',
            'В течение жизни мы съедаем около 27 тонн пищи, что равно весу семи слонов',
            'Американцы тратят на кошачий корм больше, чем на детское питание.',
            '90% женщин после входа в универмаг поворачивают направо.',
            'Озеро Байкал в Сибири является самым глубоким озером в мире. Все крупнейшие реки мира – Волга, Дон, Днепр, Енисей, Урал, Обь, Ганг, Ориноко, Амазонка, Темза, Сена и Одер – должны течь почти год, чтобы заполнить бассейн, равный по объёму озеру Байкал.',
            'В Боливии 5400 сотрудников военно-морского флота, при том, что страна не имеет выхода к морю.']
    bot.send_message(message.chat.id, random.choice(poss), reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "https://umschool.net/", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_summer == message.text)
def help_command(message):
    today = datetime.datetime.now()
    summer_2024 = datetime.datetime(2024, 6, 1, 00, 00)
    remained = (summer_2024 - today).days
    rdays = f"До лета осталось: {remained} дней."
    bot.send_message(message.chat.id, f"{rdays}", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
