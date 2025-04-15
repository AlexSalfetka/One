import tgb
import telebot
from flask import Flask
import threading


app = Flask(__name__)

@app.route('/')
def index():
    return "Бот работает!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_flask).start()
bot.polling()
