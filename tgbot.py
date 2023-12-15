import telebot
import chekker
import json

bot = telebot.TeleBot('6762792002:AAFtklPSVv7k0qe3o0WB0RF7yAF1_WlXUes')

with open('questions.json','r',encoding='utf-8') as file:
    data = json.load(file)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton("Запустить")
    markup.add(button)
    bot.send_message(message.from_user.id,
                     "Добро пожаловать в наш телеграм-бот. \n С его помощью вы можете проверить свои знания по истории. \n Для того, чтобы узнать список доступных тем, введи /topic . \n Для того, чтобы начать тест, введите /test \nдля перезапуска введите /start" ,
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_text_messages)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.text)
    global number_of_questions
    global number_of_topic
    global list_of_questions
    number_of_questions = None
    number_of_topic = None
    list_of_questions = None

    if message.text == "/start":
        start(message)
    elif message.text == "Запустить":
        start(message)
    elif message.text == "/topic":
        get_text_topic(message)
    elif message.text == "/test":
        bot.send_message(message.from_user.id,"Введите номер темы")
        get_text_topic(message)
        bot.register_next_step_handler(message, topic_check)
def get_text_topic(message):
    bot.send_message(message.from_user.id, "Список доступных тем: \n1. Народы и государства на территории современной России в древности. Русь в IX – первой трети XIII в. (КОЛ-ВО ВОПРОСОВ-28) \n2. Русь в XIII–XV вв.(КОЛ-ВО ВОПРОСОВ-12) \n3. Россия в XVI–XVII вв.(КОЛ-ВО ВОПРОСОВ-17) \n4. Россия в XVIII в.(КОЛ-ВО ВОПРОСОВ-15) \n5. Российская империя в XIX – начале XX в.(КОЛ-ВО ВОПРОСОВ-13) \n6. Россия и СССР в советскую эпоху (1917–1991)(КОЛ-ВО ВОПРОСОВ-19) \n7. Современная Российская Федерация (1991–2022)(КОЛ-ВО ВОПРОСОВ-6)")
@bot.message_handler(content_types=['text'])
def topic_check(message):
    if message.text == "/start":
        get_text_messages(message)
    elif chekker.check_topic(message.text):
        global number_of_topic
        number_of_topic=message.text
        bot.send_message(message.from_user.id, "Введите количество вопросов.")
        bot.register_next_step_handler(message, number_questions)

    else:
        bot.send_message(message.from_user.id, "Такой темы нет.")
        bot.register_next_step_handler(message, topic_check)
@bot.message_handler(content_types=['text'])
def number_questions(message):
    if message.text == "/start":
        get_text_messages(message)

    elif chekker.check_questions(message.text):
        global number_of_questions
        number_of_questions= message.text
        global list_of_questions
        list_of_questions = chekker.send_questions(int(number_of_topic), int(number_of_questions), data)
        take_answer(message)
    else:
        bot.send_message(message.from_user.id, "В блоке нет столько вопросов. Уменьши число вопросов.")
        bot.register_next_step_handler(message, number_questions)
@bot.message_handler(content_types=['text'])
def take_answer(message):
    bot.send_message(message.from_user.id, str(list_of_questions[0]) +"\n"+ str(list_of_questions[1]))
    bot.register_next_step_handler(message, asking_questions)

@bot.message_handler(content_types=['text'])
def asking_questions(message):
    global list_of_questions
    list_of_questions = list_of_questions[2:]
    if message.text == "/start":
        get_text_messages(message)
    elif message.text == list_of_questions[0]:
        bot.send_message(message.from_user.id,'Вы ответили правильно.')
        try:
            list_of_questions = list_of_questions[1:]
            take_answer(message)
        except:
            bot.send_message(message.from_user.id, " Вы ответили на все вопросы в тесте. Можете начать заново, введите номер темы.")
            get_text_topic(message)
            bot.register_next_step_handler(message, topic_check)

    else:
        bot.send_message(message.from_user.id, f'Вы ответили неправильно, правильный ответ {list_of_questions[0]}')
        try:
            list_of_questions = list_of_questions[1:]
            take_answer(message)
        except:
            bot.send_message(message.from_user.id, "Вы ответили на все вопросы в тесте. Можете начать заново, введите номер темы.")
            get_text_topic(message)
            bot.register_next_step_handler(message, topic_check)

bot.polling(none_stop=True, interval=0)

