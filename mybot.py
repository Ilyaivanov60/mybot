import logging
import ephem
import settings

from list_of_city import cities_list
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


PROXY = {
    'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}


def greet_user(update, context):
    text = 'Вызван /start' 
    usebility_comands = 'доступные команды /planet, /wordcounter, /cities'
    update.message.reply_text(text)
    update.message.reply_text(usebility_comands)


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def planets(update, context):
    print('запустилась команда /planet')
    user_text = update.message.text.split()
    planet = (user_text[1]).capitalize()
    if planet == "Mars":
      update.message.reply_text(ephem.constellation(ephem.Mars(datetime.today())))
    elif planet == "Saturn":
      update.message.reply_text(ephem.constellation(ephem.Saturn(datetime.today())))
    elif planet == "Jupiter":
      update.message.reply_text(ephem.constellation(ephem.Jupiter(datetime.today())))
    elif planet == "Moon":
      update.message.reply_text(ephem.constellation(ephem.Moon(datetime.today())))
    else:
      text = "Я не знаю такой планеты запустите команду /planet с планетой из спика (Mars, Saturn, Jupiter, Moon)"
      update.message.reply_text(text)


def wordscounter(update, context):
    user_text = update.message.text.split()
    if not user_text[1:]:
      print('мы тут')
      update.message.reply_text('Вы не ввели текс')
    else:
      update.message.reply_text(f"{len(user_text)-1} слова")


def city(update, context):
    if not cities_list:
      update.message.reply_text('Вы победили!')
    else:
      user_city = update.message.text.lower().split()[1]
      last_letter = user_city[-1]
      cities_list.remove(user_city)
      for city in cities_list:
          if city[0] == last_letter:
            update.message.reply_text(city)
            break
      cities_list.remove(city)


def main():
    mybot = Updater(settings.API_key, request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planets))
    dp.add_handler(CommandHandler("wordcounter" ,wordscounter))
    dp.add_handler(CommandHandler("cities" ,city))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
