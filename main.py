from telebot import types
import telebot.types
from openpyxl import load_workbook

TOKEN = '7541371307:AAHfbOo47fs-eSGfVN63CeCg_bUvMKRaIRI'
bot = telebot.TeleBot(TOKEN)
surname = ""
name = ""
patronymic = ""
date_birth = ""
mil_station = ""
university = ""
field_study = ""
source = ""
average_score = 0
age = 0
markup = types.InlineKeyboardMarkup(row_width=2)
markup_bottom = types.ReplyKeyboardMarkup()


@bot.message_handler(commands=["start"])
def start(message):
    sticker = open('stickers/hello.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    but_about = types.InlineKeyboardButton('О нас', callback_data='about')
    but_faq = types.InlineKeyboardButton('Часто задаваемые вопросы', callback_data='faq')
    but_ask = types.InlineKeyboardButton('Задать вопрос', callback_data='ask')
    but_reg = types.InlineKeyboardButton('Регистрация', callback_data='reg')
    markup.add(but_about, but_faq, but_ask, but_reg)

    but_about = types.KeyboardButton("О нас")
    but_faq = types.KeyboardButton("Часто задаваемые вопросы")
    but_ask = types.KeyboardButton("Задать вопрос")
    but_registration = types.KeyboardButton("Регистрация")
    markup_bottom.add(but_about, but_faq, but_ask, but_registration)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ бот научной роты Военной академии связи.".format(
                         message.from_user), parse_mode='html', reply_markup=markup)


# @bot.message_handler(content_types=['text'])
# def registration(message):
#     # if message.text == '/reg':
#         bot.send_message(message.from_user.id, "Для составления заявки необходимо заполнить некоторые данные о себе")
#         bot.send_message(message.from_user.id, "Напиши свое имя")
#         bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
#     # else:
#         bot.send_message(message.from_user.id, 'Напиши /reg')


@bot.message_handler(content_types=["text"])
def auth(message):
    if message.text == '/reg':
        bot.send_message(message.chat.id, 'Есть ли у вас высшее образование?')

        markup = types.InlineKeyboardMarkup(row_width=2)

        but_yes = types.InlineKeyboardButton("Да", callback_data='yes_university')
        but_no = types.InlineKeyboardButton("Нет", callback_data='no_university')

        markup.add(but_yes, but_no)

        bot.send_message(message.chat.id, 'У вас есть высшее образование?', reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Напиши вашу фамилию')
    bot.register_next_step_handler(message, get_surname)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Напишите ваше отчество')
    bot.register_next_step_handler(message, get_patronymic)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_patronymic(message):
    global patronymic
    patronymic = message.text
    bot.send_message(message.from_user.id, 'Напишите свою дату рождения в формате (дд.мм.гггг)')
    bot.register_next_step_handler(message, get_date_birth)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_date_birth(message):
    global date_birth
    date_birth = message.text
    bot.send_message(message.from_user.id, 'Напишите название своего военного комиссариата')
    bot.register_next_step_handler(message, get_military_station)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

def get_military_station(message):
    global mil_station
    mil_station = message.text
    bot.send_message(message.from_user.id, 'Напишите название своего ВУЗа')
    bot.register_next_step_handler(message, get_university)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

def get_university(message):
    global university
    university = message.text
    bot.send_message(message.from_user.id, 'Напишите направление подготовки в ВУЗе')
    bot.register_next_step_handler(message, get_field_study)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

def get_field_study(message):
    global field_study
    field_study = message.text
    bot.send_message(message.from_user.id, 'Напишите средний балл по диплому (х.х)')
    bot.register_next_step_handler(message, get_source)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)


def get_source(message):
    global source
    source = message.text
    bot.send_message(message.from_user.id, 'Поздравляем, ваша кандидатура будет рассмотрен для поступления '
                                           'в научную роту Военной академеии связи им С.М. Буденного')
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    add_to_excel(name, surname, patronymic)
    bot.send_message(message.from_user.id, 'Для прохождения следующих этапов отбора заполните документы')
    bot.send_document(message.chat.id, open(r'documents/Лист собеседования.docx', 'rb'))
    bot.send_document(message.chat.id, open(r'documents/Согласие.docx', 'rb'))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'yes_university':
                markup1 = types.InlineKeyboardMarkup(row_width=3)

                but_yes = types.InlineKeyboardButton("Да", callback_data='yes_age')
                but_no = types.InlineKeyboardButton("Нет", callback_data='no_age')

                markup1.add(but_yes, but_no)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Ваш возраст входит в диапазон от 18 до 30 лет?", reply_markup=markup1)

            elif call.data == 'no_university':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Извините, в научную роту рассматриваются кандидаты с наличием высшего образования")

            elif call.data == 'yes_age':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Заполните данные для формирования заявки на поступление")
                bot.send_message(call.message.chat.id, "Введите ваше имя")
                bot.register_next_step_handler(call.message, get_name)

            elif call.data == 'no_age':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Извините, в научную роту рассматриваются кандидаты в возрасте от 18 до 30 лет")

            elif call.data == "about":
                bot.send_message(call.message.chat.id, "Научные роты — российские военные подразделения, развёрнутые в структуре министерства обороны на материально-технической базе различных научно-исследовательских организаций и высших военных учебных заведений.")
            elif call.data == "faq":
                bot.send_message(call.message.chat.id, "В разработке")
            elif call.data == "ask":
                bot.send_message(call.message.chat.id, "В разработке")
            elif call.data == "reg":
                markup1 = types.InlineKeyboardMarkup(row_width=2)

                but_yes = types.InlineKeyboardButton("Да", callback_data='yes_university')
                but_no = types.InlineKeyboardButton("Нет", callback_data='no_university')

                markup1.add(but_yes, but_no)

                bot.send_message(call.message.chat.id, 'У вас есть высшее образование?', reply_markup=markup1)
    except Exception as e:
        print(repr(e))


def add_to_excel(name, surname, patronymic):
    wb = load_workbook('documents/candidates.xlsx')
    ws = wb['Sheet1']
    ws.cell(column=1, row=ws.max_row + 1, value=name)
    ws.cell(column=2, row=ws.max_row + 1, value=surname)
    ws.cell(column=3, row=ws.max_row + 1, value=patronymic)


bot.polling(none_stop=True, interval=0)
