import json
import pandas as pd
import requests
import telebot.types
import datetime

from telebot import types
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from openpyxl import load_workbook
from time import sleep

# https://api.telegram.org/bot7541371307:AAHfbOo47fs-eSGfVN63CeCg_bUvMKRaIRI/getUpdates
TOKEN = '7541371307:AAHfbOo47fs-eSGfVN63CeCg_bUvMKRaIRI7541371307:AAHfbOo47fs-eSGfVN63CeCg_bUvMKRaIRI'
bot = telebot.TeleBot(TOKEN)

time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
print(f"{time}\nProcessing...")


# page = 0
# count = 10


class Candidate:
    idUser = 0
    surname = ''
    name = ''
    patronymic = ''
    date_birth = ''
    mil_station = ''
    university = ''
    field_study = ''
    average_score = ''
    source = ''
    status = ''
    type_recruitment = ''
    find_out = ''
    phone_number = ''

    def add_to_excel(self):
        wb = load_workbook('documents/candidate.xlsx')
        sheet = wb.active
        rows_count = sheet.max_row
        data = (rows_count, self.surname, self.name, self.patronymic, self.date_birth,
                self.mil_station, self.university, self.field_study, self.average_score)
        sheet.append(data)

        wb.save(filename='documents/candidate.xlsx')


candidate = Candidate()


@bot.message_handler(commands=["start"])
def start(message):
    sticker = open('stickers/welcome_bender.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    if message.from_user.last_name is None:
        welcome_name = f'{message.from_user.first_name}'
    else:
        welcome_name = f'{message.from_user.first_name} {message.from_user.last_name}'

    welcome_msg = f'Здравствуйте, {welcome_name}\n Я - SciComBot, и я провожу отбор кандидатов в научную роту.\nВыберете интересующий Вас раздел 👇'
    go_to_main_menu(message, welcome_msg)


def go_to_main_menu(message, msg):
    kb_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    kb_about = types.KeyboardButton("❌#О_нас")
    kb_faq = types.KeyboardButton("FAQ")
    kb_tg_channel = types.KeyboardButton("Telegram-канал")
    kb_ask = types.KeyboardButton('❌Задать вопрос')
    kb_get_docs = types.KeyboardButton("Зарегистрироваться")
    kb_get_contact = types.KeyboardButton("Отправить контакт",  request_contact=True)

    kb_markup.add(kb_get_docs).row(kb_faq, kb_tg_channel, kb_about).add(kb_ask).add(kb_get_contact)
    bot.send_message(message.chat.id, msg.format(message.from_user), parse_mode='html',
                     reply_markup=kb_markup)


@bot.message_handler(content_types=["text"])
def welcome(message):
    if message.text == 'Зарегистрироваться':
        type_recruitment(message)
    elif message.text == 'Telegram-канал':
        bot.send_message(message.chat.id, "https://t.me/+ntFED2PMwUo2MDZi")
    elif message.text == 'FAQ':

        df = excel_to_2d_array('faq.xlsx')
        count = len(df) - 1
        page = 1
        question = df[1][page]
        answer = df[2][page]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                   InlineKeyboardButton(text=f'Вперёд --->',
                                        callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                            page + 1) + ",\"CountPage\":" + str(count) + "}"))
        bot.send_message(message.chat.id, text=f'<b>{question}</b>\n\n<i>{answer}</i>', parse_mode="HTML",
                         reply_markup=markup)


def type_recruitment(message):
    # kb_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    #
    # but_winter = types.KeyboardButton("Зимний")
    but_summer = types.KeyboardButton("Летний", callback_inline)
    #
    # kb_markup.add(but_winter, but_summer)

    markup = types.InlineKeyboardMarkup(row_width=2)

    but_winter = types.InlineKeyboardButton("Зимний", callback_data='winter')
    but_summer = types.InlineKeyboardButton("Летний", callback_data='summer')

    markup.add(but_winter, but_summer)

    bot.send_message(message.chat.id, 'На какой призыв вы хотите оставить заявку?', reply_markup=markup)


def is_russian(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    but_yes = types.InlineKeyboardButton("Да", callback_data='yes_russian')
    but_no = types.InlineKeyboardButton("Нет", callback_data='no_russian')

    markup.add(but_yes, but_no)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text='Являетесь ли Вы гражданином Российской Федерации?', reply_markup=markup)


def is_higher_education(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    but_yes = types.InlineKeyboardButton("Да", callback_data='yes_university')
    but_no = types.InlineKeyboardButton("Нет", callback_data='no_university')

    markup.add(but_yes, but_no)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text='Имеется ли у Вас оконченное высшее техническое образование?', reply_markup=markup)


def is_aged(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    but_yes = types.InlineKeyboardButton("Да", callback_data='yes_age')
    but_no = types.InlineKeyboardButton("Нет", callback_data='no_age')

    markup.add(but_yes, but_no)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text='Ваш возраст входит в диапазон от 18 до 30 лет?', reply_markup=markup)


def get_surname(message):
    candidate.surname = message.text
    bot.send_message(message.from_user.id, 'Напишите ваше имя')
    bot.register_next_step_handler(message, get_name)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_name(message):
    candidate.name = message.text
    bot.send_message(message.from_user.id, 'Напишите ваше отчество')
    bot.register_next_step_handler(message, get_patronymic)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_patronymic(message):
    candidate.patronymic = message.text
    bot.send_message(message.from_user.id, 'Напишите свою дату рождения в формате (дд.мм.гггг)')
    bot.register_next_step_handler(message, get_date_birth)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_date_birth(message):
    try:
        datetime.datetime.strptime(message.text or "", "%d.%m.%Y")
        candidate.date_birth = message.text
        bot.send_message(message.from_user.id, 'Напишите название своего военного комиссариата')
        bot.register_next_step_handler(message, get_military_station)
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    except ValueError:
        bot.send_message(message.from_user.id, 'Введена некорректная дата, попробуйте снова')
        bot.register_next_step_handler(message, get_date_birth)


def get_military_station(message):
    candidate.mil_station = message.text
    bot.send_message(message.from_user.id, 'Напишите название своего ВУЗа')
    bot.register_next_step_handler(message, get_university)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_university(message):
    candidate.university = message.text
    bot.send_message(message.from_user.id, 'Напишите направление подготовки в ВУЗе')
    bot.register_next_step_handler(message, get_field_study)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_field_study(message):
    candidate.field_study = message.text
    bot.send_message(message.from_user.id, 'Напишите средний балл по диплому (х.х)')
    bot.register_next_step_handler(message, get_average_score)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_average_score(message):
    try:
        score = float(message.text)
        if score > 5 or score < 4:
            bot.send_message(message.from_user.id, 'Ваш средний балл не соответствует требованиям.\n'
                                                   'В научную роту рассматриваются кандидаты со средним баллом не менее 4.0')
            return
        candidate.average_score = message.text
        bot.send_message(message.from_user.id, 'Откуда вы узнали о нас?')
        bot.register_next_step_handler(message, get_find_out)
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    except ValueError:
        bot.send_message(message.from_user.id, 'Введен некорректный балл, попробуйте снова')
        bot.register_next_step_handler(message, get_average_score)


def get_find_out(message):
    candidate.find_out = message.text

    kb_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)


    kb_get_contact = types.KeyboardButton("Отправить номер", request_contact=True)

    kb_markup.add(kb_get_contact)
    bot.send_message(message.chat.id, parse_mode='html',
                     text='Для связи с вами, нам необходимо получить ваш номер телефона. Нажмите кнопку в меню или напишите его в чат',
                     reply_markup=kb_markup)

    bot.register_next_step_handler(message, send_docs)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def send_docs(message):

    bot.send_message(message.from_user.id, 'Поздравляем, ваша кандидатура будет рассмотрена для поступления '
                                           'в научную роту Военной академеии связи им С.М. Буденного')
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    candidate.add_to_excel()
    # bot.send_message(message.from_user.id, 'Для прохождения следующих этапов отбора заполните документы')
    go_to_main_menu(message, 'Для прохождения следующих этапов отбора заполните документы')
    bot.send_document(message.chat.id, open(r'documents/Лист собеседования.docx', 'rb'))
    bot.send_document(message.chat.id, open(r'documents/Согласие.docx', 'rb'))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    req = call.data.split('_')

    try:
        if call.message:
            if call.data == 'winter':
                candidate.type_recruitment = 'Зимний'
                is_russian(call.message)
                # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            elif call.data == 'summer':
                candidate.type_recruitment = 'Летний'
                is_russian(call.message)
                # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            elif call.data == 'yes_russian':
                is_higher_education(call.message)
            elif call.data == 'no_russian':

                go_to_main_menu(call.message,
                                "Извините, наличие гражданства Российской Федерации "
                                "является обязательным условием для отбора в научную роту")
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            elif call.data == 'yes_university':
                is_aged(call.message)
            elif call.data == 'no_university':
                go_to_main_menu(call.message,
                                "Извините, наличие Высшего технического образования является "
                                "обязательным условием для отбора в научную роту")
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            elif call.data == 'yes_age':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Заполните данные для формирования заявки на поступление")
                bot.send_message(call.message.chat.id, 'Укажите вашу фамилию')
                bot.register_next_step_handler(call.message, get_surname)
            elif call.data == 'no_age':
                go_to_main_menu(call.message,
                                'В Соответствии с положениями п.п."а", пункта 1, статьи 22 \"Граждане, подлежащие призыву на военную службу\"'
                                'Федерального закона от 28.03.1998 N 53-ФЗ (ред. от 02.10.2024) \"О воинской обязанности и военной службе\",'
                                'призыву  на  военную службу подлежат граждане мужского пола в возрасте от 18 до 30 лет, состоящие на воинском учете '
                                'или не состоящие, но обязанные состоять на воинском учете и не пребывающие в запасе ')
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            elif call.data == 'unseen':
                bot.delete_message(call.message.chat.id, call.message.message_id)
            elif 'pagination' in call.data:

                # Расспарсим полученный JSON
                json_string = json.loads(req[0])

                df = excel_to_2d_array('faq.xlsx')
                count = len(df) - 1
                page = json_string['NumberPage']

                question = df[1][page]
                answer = df[2][page]

                # Пересоздаем markup
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))

                # markup для первой страницы
                if page == 1:
                    markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                               InlineKeyboardButton(text=f'Вперёд --->',
                                                    callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                        page + 1) + ",\"CountPage\":" + str(count) + "}"))
                # markup для второй страницы
                elif page == count:
                    markup.add(InlineKeyboardButton(text=f'<--- Назад',
                                                    callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                        page - 1) + ",\"CountPage\":" + str(count) + "}"),
                               InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))
                # markup для остальных страниц
                else:
                    markup.add(InlineKeyboardButton(text=f'<--- Назад',
                                                    callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                        page - 1) + ",\"CountPage\":" + str(count) + "}"),
                               InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                               InlineKeyboardButton(text=f'Вперёд --->',
                                                    callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                        page + 1) + ",\"CountPage\":" + str(count) + "}"))

                bot.edit_message_text(text=f'<b>{question}</b>\n\n<i>{answer}</i>', parse_mode='HTML',
                                      reply_markup=markup, chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
            elif call.data == 'send_phone_number':
                bot.register_next_step_handler(call.message, send_docs)


    except Exception as e:
        print(repr(e))


def excel_to_2d_array(name_doc):
    wb = load_workbook('documents/faq.xlsx')
    sheet = wb.active
    df = pd.DataFrame(sheet.values)
    return df


bot.infinity_polling()