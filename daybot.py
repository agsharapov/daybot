import os
import logging
from requests import get
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
from datetime import datetime

weekdays = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье'
}

load_dotenv()
token = os.getenv('TOKEN')

logging.basicConfig(
    level=logging.INFO,
    encoding='utf=8',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

URL = 'http://worldtimeapi.org/api/timezone/Europe/Moscow/'


def present_day():
    try:
        response = get(URL)
        today = response.json()
        date = datetime.strptime(
            today.get('datetime'),
            '%Y-%m-%dT%H:%M:%S.%f+03:00'
        )
        date = date.strftime("%d.%m")
        weekday = weekdays[today.get('day_of_week')-1]
    except Exception as error:
        logging.error(f'Ошибка: {error}. Код ответа: {response.status_code}')
        today = datetime.today()
        date = today.strftime("%d.%m")
        weekday = weekdays[today.weekday()]
    return f'Сегодня {date}, {weekday}.'


def reply(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['Какой сегодня день?']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat.id,
        present_day(),
        reply_markup=button
    )


def main():
    updater = Updater(token)
    updater.dispatcher.add_handler(
        CommandHandler('start', reply)
    )
    updater.dispatcher.add_handler(
        CommandHandler('today', reply)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text('Какой сегодня день?'), reply)
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
