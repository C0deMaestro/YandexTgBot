import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from speechkit import Session,ShortAudioRecognition
import requests

TOKEN = "6363656442:AAHGEacNHFZO_eFlpu-t5BXYihQTkCRULXg"
oauth_token = "y0_AgAAAAAIbQyoAATuwQAAAADn6fFPanlxeFjFR1Wdp-eir0q-Kz6X-rk"
catalog_id = "b1gp5vbua4qdjpm28bbe"
saved_messages_file = "saved_messages.txt"

session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
bot = telebot.TeleBot(TOKEN)

save_state = {}


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    bot.send_message(message.chat.id, f"Привет, {user.first_name}! Это бот, который поможет нам познакомиться. "
                                      "Чтобы узнать больше обо мне, используйте команды или кнопки ниже.")
    show_menu(message)
    show_commands(message.chat.id)

# Вызов меню
@bot.message_handler(commands=['menu'])
def show_menu(message):
    show_options(message.chat.id)

# Следующий шаг
@bot.message_handler(commands=['mygit'])
def show_mygit(message):
    bot.send_message(message.chat.id,f"Ссылка на мой гит:\nhttps://github.com/C0deMaestro?tab=repositories")

# Ссылка на гит
@bot.message_handler(commands=['nextstep'])
def next_step(message):
    bot.send_message(message.chat.id,f"Сохраню следующее сообщение, если вы не против...")
    save_state[message.chat.id] = True


# Сохранение следующего сообщения пользователя
@bot.message_handler(func=lambda message: message.chat.id in save_state and save_state[message.chat.id])
def save_next_message(message):
    with open(saved_messages_file, "a", encoding="utf-8") as file:
        file.write(f"{message.from_user.username}: {message.text}\n")
    bot.send_message(message.chat.id, "Сохранено! Спасибо.")
    save_state[message.chat.id] = False

# Отображение доступных опций
def show_options(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Моё последнее селфи", callback_data='latest_selfie'),
                 InlineKeyboardButton("Фото из старшей школы", callback_data='school_photo'))
    keyboard.row(InlineKeyboardButton("Моё главное увлечение", callback_data='hobby'),
                 InlineKeyboardButton("Слушать войс", callback_data='voice'))

    bot.send_message(chat_id, 'Выберите опцию:', reply_markup=keyboard)

# Отображение списка команд
def show_commands(chat_id):
    commands = [
        "/menu, Голосом : 'меню', - Меню с опциями",
        "/nextstep, Голосом : 'следующий шаг', - Рассказать о следующих шагах",
        "/mygit, Голосом : 'ссылка на гит', - Получить ссылку на git"
    ]

    commands_text = "Список команд (их можно вызывать голосом!):\n" + "\n".join(commands)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for command in commands:
        keyboard.add(KeyboardButton(command))

    bot.send_message(chat_id, commands_text, reply_markup=keyboard)


# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def button_handler(call):
    chat_id = call.message.chat.id
    option = call.data

    if option == 'latest_selfie':
        send_latest_selfie(chat_id)
    elif option == 'school_photo':
        send_school_photo(chat_id)
    elif option == 'hobby':
        send_hobby_post(chat_id)
    elif option == 'voice':
        send_voice_options(chat_id)
    elif option == 'gpt_voice':
        send_gpt_voice(chat_id)
    elif option == 'sql_nosql_voice':
        send_sql_nosql_voice(chat_id)
    elif option == 'love_story_voice':
        send_love_story_voice(chat_id)

    bot.answer_callback_query(call.id)


# Отправка последнего селфи
def send_latest_selfie(chat_id):
    bot.send_photo(chat_id, photo=open('D:\\YndxTestBot\\photo\\latest_selfie.jpg', 'rb'))

# Отправка фото из старшей школы
def send_school_photo(chat_id):
    bot.send_photo(chat_id, photo=open('D:\\YndxTestBot\\photo\\school_photo.jpg', 'rb'))

# Отправка поста о главном увлечении
def send_hobby_post(chat_id):
    post = '''**Доброе утро, добрый день или добрый вечер, читающему этот пост!** 👋

    🏀 Кроме программирования, моё главное увлечение - это **баскетбол**! 

    ❤️ Я очень люблю эту игру с мячом. Играл за школу, город, область и университет. Пока на этом всё. 
    Если у вас есть команда, за которую я мог бы поиграть, то знайте, что мне нужно пополнять список! 😉
        '''
    bot.send_message(chat_id, post, parse_mode='Markdown')

# Обработчик сообщений с текстом
@bot.message_handler(func=lambda message: message.text.lower() == '/nextstep')
def text_message_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Дальнейшие шаги...')

# Отправка войсовых сообщений
def send_voice_options(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Объясняю своей бабушке, что такое GPT", callback_data='gpt_voice'))
    keyboard.row(InlineKeyboardButton("Разница между SQL и NoSQL", callback_data='sql_nosql_voice'))
    keyboard.row(InlineKeyboardButton("История первой любви", callback_data='love_story_voice'))

    bot.send_message(chat_id, 'Выберите вариант:', reply_markup=keyboard)

# Отправка голосового сообщения "Объясняю своей бабушке, что такое GPT"
def send_gpt_voice(chat_id):
    voice_path = 'D:\\YndxTestBot\\photo\\gpt_voice.ogg'  # Путь к голосовому сообщению
    with open(voice_path, 'rb') as voice:
        bot.send_voice(chat_id, voice)

# Отправка голосового сообщения "Разница между SQL и NoSQL"
def send_sql_nosql_voice(chat_id):
    voice_path = 'D:\\YndxTestBot\\photo\\sql_nosql_voice.ogg'  # Путь к голосовому сообщению
    with open(voice_path, 'rb') as voice:
        bot.send_voice(chat_id, voice)

# Отправка голосового сообщения "История первой любви"
def send_love_story_voice(chat_id):
    voice_path = 'D:\\YndxTestBot\\photo\\love_story_voice.ogg'  # Путь к голосовому сообщению
    with open(voice_path, 'rb') as voice:
        bot.send_voice(chat_id, voice)

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    # Получение файла голосового сообщения
    file_info = bot.get_file(message.voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    print(file_url)
    # Загрузка файла на локальный сервер
    audio_file = download_voice_file(file_url)
    with open('voice_message.oga', 'rb') as f:
        data = f.read()
    # Распознавание речи
    recognizeShortAudio = ShortAudioRecognition(session)

    # Передаем файл и его формат в метод `.recognize()`,
    # который возвращает строку с текстом
    text = recognizeShortAudio.recognize(
        data, sampleRateHertz='48000')

    flag = True

    if text.lower() == "меню":
        flag = False
        show_menu(message)
    elif "ссылка на ги" in text.lower():
        flag = False
        show_mygit(message)
    elif text.lower() == "следующий шаг":
        flag = False
        next_step(message)

    # Отправка распознанного текста пользователю
    if flag:
        bot.send_message(message.chat.id, f"Распознанный текст:\n{text}")

def download_voice_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        audio_file = "voice_message.oga"
        with open(audio_file, "wb") as file:
            file.write(response.content)
        return audio_file
    else:
        return None

# Запуск бота
bot.polling()