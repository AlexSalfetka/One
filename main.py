from tgb import bot  # Импортируем объект бота из bot_logic.py

if __name__ == "__main__":
    bot.polling(non_stop=True)  # Запускаем бота, чтобы он начал обрабатывать сообщения
