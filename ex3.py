import telebot
from openai import OpenAI

# Ваш токен, который вы получили от @BotFather
API_TOKEN = '7120255190:AAEwgDoaDOE1P1740WXOuAdEOAH0rBSbL8M'
OPENAI_API_KEY = 'sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I'

# Инициализация клиента OpenAI
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)


# Обрабатываем команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш новый бот. Чем могу помочь?")


# Обрабатываем команду /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Команды, которые я понимаю:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить список команд\n"
        "/perevorot - Перевернуть текст\n"
        "/caps - Преобразовать текст в заглавные буквы\n"
        "/count - Подсчитать количество слов и символов в тексте\n"
        # Добавьте сюда другие команды, если будут добавлены в будущем
    )
    bot.reply_to(message, help_text)


# Обрабатываем команду /perevorot
@bot.message_handler(commands=['perevorot'])
def perevorot(message):
    # Получаем текст, который нужно перевернуть, удаляя команду из сообщения
    text_to_reverse = message.text[len('/perevorot '):]
    # Переворачиваем текст
    reversed_text = text_to_reverse[::-1]
    bot.reply_to(message, reversed_text)


# Обрабатываем команду /caps
@bot.message_handler(commands=['caps'])
def caps(message):
    # Получаем текст, который нужно преобразовать в заглавные буквы, удаляя команду из сообщения
    text_to_caps = message.text[len('/caps '):]
    # Преобразуем текст в заглавные буквы
    caps_text = text_to_caps.upper()
    bot.reply_to(message, caps_text)


# Обрабатываем команду /count
@bot.message_handler(commands=['count'])
def count(message):
    # Получаем текст, который нужно проанализировать, удаляя команду из сообщения
    text_to_count = message.text[len('/count '):]
    # Подсчитываем количество слов и символов
    word_count = len(text_to_count.split())
    char_count = len(text_to_count)
    response = f"Количество слов: {word_count}\nКоличество символов: {char_count}"
    bot.reply_to(message, response)


def chat_with_gpt3(message_text):
    messages = [{"role": "user", "content": message_text}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages)
    # Получаем текст ответа
    reply = response.choices[0].message.content
    return reply


# Обрабатываем любые другие сообщения
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = chat_with_gpt3(message.text)
    bot.reply_to(message, response)


# Запуск бота
bot.polling()