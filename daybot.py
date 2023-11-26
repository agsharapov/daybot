import os
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

def present_day():
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
        CommandHandler('command1', reply)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text('Какой сегодня день?'), reply)
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
