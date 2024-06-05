import telebot

from gtts import gTTS
from io import BytesIO

# Укажите токен вашего бота
TOKEN = '7120255190:AAEwgDoaDOE1P1740WXOuAdEOAH0rBSbL8M'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    tts = gTTS(text=message.text, lang='ru')
    voice = BytesIO()
    tts.write_to_fp(voice)
    voice.seek(0)
    bot.send_voice(chat_id=message.chat.id, voice=voice)


if __name__ == '__main__':
    bot.polling(non_stop=True)
