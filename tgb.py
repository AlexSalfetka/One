import telebot
from telebot import types
import sys

try:
    import ssl
except ImportError:
    print("SSL module is not available. Bot cannot run without SSL.", file=sys.stderr)
    sys.exit(1)

bot = telebot.TeleBot('8198227498:AAFn7CBrYNa7YU7_uO2BwFgNY5gBNvjznT4')

# Состояния пользователей
user_state = {}
user_data = {}
GROUP_CHAT_ID = -1002606392125

# Главное меню
main_menu_buttons = ['📢 О нас', '🛒 Оформить заказ', '💰 Цены', '❓ FAQ', '☎️ Связаться с менеджером']

def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('📢 О нас'), types.KeyboardButton('🛒 Оформить заказ'))
    markup.row(types.KeyboardButton('💰 Цены'), types.KeyboardButton('❓ FAQ'))
    markup.row(types.KeyboardButton('☎️ Связаться с менеджером'))
    bot.send_message(chat_id,
                     "🤝 Добро пожаловать в TrustBoost — сервис, который помогает вашему бизнесу становиться более заметным с помощью наших отзывов. Используйте меню ниже для выбора услуги. Если вам нужно больше информации или помощь, наш менеджер всегда на связи 💬",
                     reply_markup=markup)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_state.pop(message.chat.id, None)
    user_data.pop(message.chat.id, None)
    send_main_menu(message.chat.id)

# Обработка текстов
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # Если пользователь нажал кнопку главного меню — сбрасываем состояние
    if text in main_menu_buttons:
        user_state.pop(chat_id, None)
        user_data.pop(chat_id, None)

    if text == '📢 О нас':
        bot.send_message(chat_id, """
TrustBoost — опытная команда, что помогает компаниям и частным лицам повышать доверие клиентов с помощью положительных отзывов. 📝

Пишем уникальные тексты, учитываем особенности вашего бизнеса и всегда соблюдаем сроки.🤝

Работаем быстро, конфиденциально и с акцентом на качество!
С нами ваша репутация станет сильнее, а продажи — выше. 📈""")

    elif text == '🛒 Оформить заказ':
        user_state[chat_id] = 'platform'
        user_data[chat_id] = {}
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton('Авито', callback_data='platform_avito'),
            types.InlineKeyboardButton('Яндекс карты', callback_data='platform_yandex')
        )
        markup.row(
            types.InlineKeyboardButton('Гугл карты', callback_data='platform_google'),
            types.InlineKeyboardButton('2ГИС', callback_data='platform_2gis')
        )
        markup.row(
            types.InlineKeyboardButton('Отзовик', callback_data='platform_otzovik'),
            types.InlineKeyboardButton('Профи.ру', callback_data='platform_profi')
        )
        markup.row(
            types.InlineKeyboardButton('Другое', callback_data='platform_other')
        )
        bot.send_message(chat_id, "🛒 Отлично! На какой платформе нужны отзывы?", reply_markup=markup)

    elif text == '💰 Цены':
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('Авито', callback_data='price_avito'),
            types.InlineKeyboardButton('Гугл карты', callback_data='price_google'),
            types.InlineKeyboardButton('Яндекс карты', callback_data='price_yandex'),
            types.InlineKeyboardButton('2ГИС', callback_data='price_2gis'),
            types.InlineKeyboardButton('Отзовик', callback_data='price_otzovik'),
            types.InlineKeyboardButton('Профи.ру', callback_data='price_profi'),
            types.InlineKeyboardButton('Другое', callback_data='price_other')
        )
        bot.send_message(chat_id, "💰 Выберите платформу, чтобы узнать цену:", reply_markup=markup)

    elif text == '❓ FAQ':
        markup = types.InlineKeyboardMarkup(row_width=1)  # Устанавливаем row_width=1 для отображения в столбик
        markup.add(
            types.InlineKeyboardButton('⏱️ Сроки выполнения?', callback_data='faq_1'),
            types.InlineKeyboardButton('🛡 Антиблокировка?', callback_data='faq_2'),
            types.InlineKeyboardButton('💳 Оплата?', callback_data='faq_3'),
            types.InlineKeyboardButton('👤 Кто пишет отзывы?', callback_data='faq_4'),
            types.InlineKeyboardButton('🛠 Что если отзыв удалят?', callback_data='faq_5')
        )
        bot.send_message(chat_id, "❓ Выберите вопрос, чтобы получить ответ:", reply_markup=markup)

    elif text == '☎️ Связаться с менеджером':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='💬 Написать менеджеру', url='https://t.me/trustboost_manager')
        markup.add(btn)
        bot.send_message(chat_id,
                         """У вас есть вопросы или хотите обсудить детали заказа лично? 🤔
Наш менеджер на связи и готов помочь!""",
                         reply_markup=markup)

    elif user_state.get(chat_id) == 'link':
        user_data[chat_id]['link'] = text
        user_state[chat_id] = 'count'
        bot.send_message(chat_id, "🔢 Сколько отзывов вы хотите заказать?")

    elif user_state.get(chat_id) == 'count':
        user_data[chat_id]['count'] = text
        user_state[chat_id] = 'business'
        bot.send_message(chat_id, "🏢 Чем занимается ваш бизнес?")

    elif user_state.get(chat_id) == 'business':
        user_data[chat_id]['business'] = text
        user_state[chat_id] = 'wishes'
        bot.send_message(chat_id, "📝 Есть ли особые пожелания к тексту отзывов?")

    elif user_state.get(chat_id) == 'wishes':
        user_data[chat_id]['wishes'] = text
        bot.send_message(chat_id, "✅ Спасибо! Ваш заказ отправлен менеджеру.")

        # Отправка в группу
        data = user_data[chat_id]
        summary = f"📥 Новый заказ от @{message.from_user.username or 'пользователя'}\n\n"
        summary += f"Платформа: {data.get('platform')}\n"
        summary += f"Ссылка: {data.get('link')}\n"
        summary += f"Количество отзывов: {data.get('count')}\n"
        summary += f"Бизнес: {data.get('business')}\n"
        summary += f"Пожелания: {data.get('wishes')}"

        bot.send_message(GROUP_CHAT_ID, summary)

        # После завершения заказа, отправляем в главное меню
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton('📢 О нас'), types.KeyboardButton('🛒 Оформить заказ'))
        markup.row(types.KeyboardButton('💰 Цены'), types.KeyboardButton('❓ FAQ'))
        markup.row(types.KeyboardButton('☎️ Связаться с менеджером'))
        bot.send_message(chat_id,
                         "🛒 Ваш заказ успешно оформлен! Вы можете оформить новый заказ или ознакомиться с другими услугами.",
                         reply_markup=markup)

# Обработка выбора платформы
@bot.callback_query_handler(func=lambda call: call.data.startswith('platform_'))
def handle_platform(call):
    chat_id = call.message.chat.id
    platform = call.data.split('_')[1].capitalize()
    user_data[chat_id] = {'platform': platform}
    user_state[chat_id] = 'link'
    bot.send_message(chat_id, f"🔗 Пришлите ссылку на ваш товар/услугу/профиль на {platform}.")

# Обработка кнопок с ценами
@bot.callback_query_handler(func=lambda call: call.data.startswith('price_'))
def handle_price_buttons(call):
    chat_id = call.message.chat.id
    platform_key = call.data.split('_')[1].lower()

    price_texts = {
        'avito': 'Цена отзыва: 300 рублей. От 10 шт — 270 р.',
        'google': 'Цена отзыва: 500 рублей. От 10 шт — 450 р.',
        'yandex': 'Цена отзыва: 500 рублей. От 10 шт — 450 р.',
        '2gis': 'Цена отзыва: 500 рублей. От 10 шт — 450 р.',
        'profi': 'Цена отзыва: 400 рублей. От 10 шт — 360 р.',
        'otzovik': 'Цена отзыва: 700 рублей. От 10 шт — 630 р.',
        'other': 'Цена обсуждается с менеджером.'
    }

    platform_names = {
        'avito': 'Авито',
        'google': 'Гугл карты',
        'yandex': 'Яндекс карты',
        '2gis': '2ГИС',
        'profi': 'Профи.ру',
        'otzovik': 'Отзовик',
        'other': 'Другое'
    }

    # Получаем платформу и цену без переноса строк
    platform = platform_names[platform_key]
    price = price_texts[platform_key]

    bot.answer_callback_query(call.id)
    bot.send_message(chat_id, f"<b>{platform}</b>\n{price}", parse_mode='HTML')

# Обработка выбора FAQ
@bot.callback_query_handler(func=lambda call: call.data.startswith('faq_'))
def handle_faq(call):
    chat_id = call.message.chat.id
    question = call.data.split('_')[1]

    if question == '1':
        answer = """ 
🕒 Обычно от 1 до 3 дней, зависит от объема заказа."""
    elif question == '2':
        answer = """ 
👥 Мы тщательно создаём уникальные тексты вручную. Отзывы пишут реальные исполнители со своих настоящих аккаунтов."""
    elif question == '3':
        answer = """ 
💵 Новым клиентам — предоплата 100%. Постоянным клиентам возможна оплата по факту."""
    elif question == '4':
        answer = """ 
✍️ Наши отзывы — это работы реальных людей! Каждый отзыв пишется вручную и только с учётом особенностей вашего бизнеса."""
    elif question == '5':
        answer = """ 
🧑‍💻 В случае удаления отзыва, мы пишем бесплатно новый."""

    bot.send_message(chat_id, answer)

if __name__ == "__main__":
    bot.polling(none_stop=True)


















