import telebot
from flask import Flask
import threading

bot = telebot.TeleBot("8198227498:AAFn7CBrYNa7YU7_uO2BwFgNY5gBNvjznT4")

app = Flask(__name__)

@app.route('/')
def index():
    return "Бот работает!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет!")

threading.Thread(target=run_flask).start()
bot.polling()
