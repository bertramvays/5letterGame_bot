from telegram import Update
from telegram.ext import ContextTypes
from middlewares.input_lists_filter import no, letter_position_filter
from configs.config_bot import words, post_size
from service_messages import *
from configs.config_log import logCommands, logInput


async def clear_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Очистка ввода пользователя
    context.user_data['letters_no'].clear()
    context.user_data["known_position"].clear()
    context.user_data["unknown_position"].clear()
    logCommands.info(f' Пользователь {update.effective_user.id} нажал /clear_input')
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=clear_msg, parse_mode='HTML')


async def filter_words(update: Update, context: ContextTypes.DEFAULT_TYPE, n=post_size):
    # Функция применяет фильтры для вывода слов
    result = []
    for w in words:
        if no(w, context.user_data['letters_no']):
            if letter_position_filter(w, known_position=context.user_data['known_position'],
                                      unknown_position=context.user_data['unknown_position']):
                result.append(w)
    logInput.info(f'Пользователь {update.effective_user.id},'
                  f' список отсутствующих букв - {context.user_data["letters_no"]}, '
                  f'список букв с известными позициями - {context.user_data["known_position"]}, '
                  f'список букв с неизвестными позициями - {context.user_data["unknown_position"]},')
    # Разбиение массива слов на несколько сообщений заданного размера
    for i in [result[i:n + i] for i in range(0, len(result), n)]:
        message = ', '.join(i)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=message)
