import telebot
from config import TOKEN, keys
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message):
    bot_info = (
        "Привет! Я бот для расчета стоимости валют.\n\n"
        "Для получения курса валют введите запрос в формате:\n"
        "<имя требуемой валюты> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.\n\n"
        "Пример запроса:\n"
        "Рубль Евро 100\n\n"
        "Чтобы узнать список всех доступных валют, воспользуйтесь командой:\n"
        "/values"
    )
    bot.send_message(message.chat.id, bot_info)


@bot.message_handler(commands=['values'])
def get_values(message):
    values_info = "Список доступных валют:"
    for key in keys.keys():
        values_info = "\n".join((values_info, key))
    bot.reply_to(message, values_info)


@bot.message_handler(func=lambda message: True)
def converter(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Некорректно введен запрос.")

        base, quote, amount = values

        base = base.capitalize()
        quote = quote.capitalize()

        total_amount = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}")
    else:
        text = f'Стоимость {amount} "{base}" в "{quote}" равна {total_amount}'
        bot.send_message(message.chat.id, text)


print("Bot started")
bot.polling()
