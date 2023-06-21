import pytube
import os
import telebot
from telebot import types
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('TG_TOKEN')
bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton("Скачать аудио")
  btn2 = types.KeyboardButton("Скачать видео")
  markup.add(btn1, btn2)
  bot.send_message(message.from_user.id, "Здравствуйте. Вставьте ссылку на видео.", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def video(message):
  try:
    yt = pytube.YouTube(message.text)
  except:
    bot.send_message(message.from_user.id, 'Извините. Некорректная ссылка. Проверьте правильность ссылки.')
    return
  bot.send_message(message.from_user.id, 'Начинаю скачивание. Подождите...')
  audio = yt.streams.get_audio_only().download()
  base, ext = os.path.splitext(audio)
  new_file = base + '.mp3'
  os.rename(audio, new_file)
  audio_op = open(new_file, 'rb')
  bot.send_audio(message.chat.id, audio_op)
  audio_op.close()
  os.remove(new_file)
bot.infinity_polling()
