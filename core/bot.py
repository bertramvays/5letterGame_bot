from telegram.ext import ApplicationBuilder, Application, CommandHandler, MessageHandler, filters
from configs.config_bot import config
from handlers.basics import get_start, get_help
from handlers.user_input import input_letter_pos
from handlers.words_utils import clear_input, filter_words
from service_messages import *
import csv

BOT_TOKEN = config.bot_token.get_secret_value()
ADMIN_ID = config.admin_id


async def post_start(application: Application):
    # функция отправляет сообщение админу при запуске бота.
    await application.bot.send_message(chat_id=ADMIN_ID,
                                       text=bot_startup_msg)


async def post_shutdown(application: Application):
    # функция отправляет сообщение админу при запуске бота.
    with open('bot_users.csv', 'a+') as f:
        w = csv.writer(f)
        w.writerow(application.bot_data.keys())
        w.writerow(application.bot_data.values())
    await application.bot.send_message(chat_id=ADMIN_ID,
                                       text=bot_shutdown_msg)


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_start).post_stop(post_shutdown).build()
    start_handler = CommandHandler(['start', ], get_start)
    application.add_handler(start_handler)
    help_handler = CommandHandler(['help', ], get_help)
    application.add_handler(help_handler)
    show_words_handler = CommandHandler(['words', ], filter_words)
    application.add_handler(show_words_handler)
    clear_handler = CommandHandler('clear_input', clear_input)
    application.add_handler(clear_handler)
    letter_input_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), input_letter_pos)
    application.add_handler(letter_input_handler)
    application.run_polling()
