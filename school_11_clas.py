import telebot
from telebot import types

bot = telebot.TeleBot(r'5704680403:AAGblA4kuv99uoI32gYaXVaiDToU324Fmbc')

first_stage = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Розклад уроків', 'Розклад дзвінків', "ДЗ",
                                                                  'Розробнику Антону на каву))')
# call schedule
call_schedule = [r'AgACAgIAAxkBAANAY2fvF4YsiX9FyO3WV2K784NDo94AAlLBMRvLaEBLGWyguMlerYYBAAMCAAN5AAMrBA']

# timetable
timetable = [r'AgACAgIAAxkBAAIBoWNrubZqWFNNDGx0HfQ0cXBBWdohAAIbwTEbO7NhSx6c1VV1KXAZAQADAgADeQADKwQ']

# homework Фізика , вправа 11 %1 вправа 12 %5
homework = ['Геометрія - 5.16 , 5.20', 'Фізика , вправа 11 %1 вправа 12 %5']

subject_list = ['Алгебра'.lower(), "Геометрія".lower(), "Фізика".lower(),
                'Укр.мова'.lower(), "Укр.літ".lower(), "Зар.літ".lower(),
                "Англ.мова".lower(), "Географія".lower(), "Історія".lower(),
                "Нім.мова".lower(), "Хімія".lower(), "Біологія".lower(),
                "Астрономія".lower(), "Ф.Г.".lower(), "ЗУ".lower()]

# remove home task in list
markup_for_homework = ['Видалити']

# in these variables are saving current subject
current_subject = ''

# admin list
admin_list = [735931812, 897816012]
checker = False

# for admin inline button
markup_inline = types.InlineKeyboardMarkup()
item_yes = types.InlineKeyboardButton(text='Замінити ?', callback_data='yes')
markup_inline.add(item_yes)


def make_category(lister):
    inl_keyboard = types.InlineKeyboardMarkup()

    list_button = []
    for dir_name in lister:
        list_button.append(types.InlineKeyboardButton(dir_name.title(), callback_data=dir_name.lower()))

    for i in range(0, len(list_button), 3):
        inl_keyboard.add(*list_button[i: i + 3])

    return inl_keyboard


@bot.message_handler(commands=['start', 'new'])
def get_start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'ку, {message.from_user.first_name}', reply_markup=first_stage)

    if message.from_user.id in admin_list:

        if message.text == '/new':
            bot.send_message(message.chat.id, 'надішли ДЗ', reply_markup=make_category(subject_list))


@bot.message_handler(content_types=['text'])
def get_message(message):
    global checker, homework

    if message.from_user.id in admin_list:
        checker = True

    if message.text == 'Розробнику Антону на каву))':
        bot.send_message(message.chat.id, 'monobank -\n4441114462072339')

    elif message.text == 'Розклад уроків':
        if len(timetable) < 7:
            bot.send_photo(message.chat.id, timetable[-1],
                           reply_markup=markup_inline if checker else first_stage)
        else:
            del timetable[0]
            bot.send_photo(message.chat.id, timetable[-1],
                           reply_markup=markup_inline if checker else first_stage)

    elif message.text == 'Розклад дзвінків':

        bot.send_photo(message.chat.id, call_schedule[-1])

    elif message.text == "ДЗ":
        if homework:
            for i in homework:
                bot.send_message(message.chat.id, f'{i}',
                                 reply_markup=make_category(markup_for_homework) if checker else first_stage)
        else:
            bot.send_message(message.chat.id, 'Поки немає ДЗ')


def get_mes(message):
    homework.append(f'{current_subject} - {message.text}')
    bot.send_message(message.chat.id, 'Домашка успішно збереженна', reply_markup=first_stage)


@bot.callback_query_handler(lambda a: True)
def get_query(query):
    if query.data == 'yes':
        bot.send_message(query.message.chat.id, 'кинь новий розклад')

        @bot.message_handler(content_types=['photo'])
        def get_photo(message):
            global timetable
            timetable.append(message.photo[-1].file_id)
            bot.send_message(message.chat.id, 'успішно збережено')

    elif query.data == 'видалити':

        for el in homework:
            if el == query.message.text:
                homework.remove(el)

    elif query.data in subject_list:
        global current_subject

        current_subject = ''
        current_subject += query.data
        msg = bot.send_message(query.message.chat.id, f'{query.data}')

        bot.register_next_step_handler(msg, get_mes)


bot.polling()
