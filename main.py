import telebot
from tokens import TOKEN
from extensions import APIException, Convertor

bot = telebot.TeleBot(TOKEN)  # https://t.me/Exofcurbot


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = " Привет. \n Для расчета обмена валюты введите команду: \n " \
           "<имя валюты цену которой он хочет узнать><имя валюты в которой надо узнать цену первой валюты>" \
           "<количество первой валюты> (Пример: евро рубль 2000 )." \
           " \n Для просмотра поддерживаемых валют введите: /values "

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    bot.reply_to(message, Convertor.AvailCurr())


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    val = message.text.split(' ')
    try:
        if val[0][:1] == "/":
            raise APIException('Команда не поддерживается!')

        if len(val) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*val)

    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception:
        bot.reply_to(message, "Неизвестная ошибка")
    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)
