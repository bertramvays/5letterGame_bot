from telegram import Update
from telegram.ext import ContextTypes
from service_messages import *
from configs.config_log import logMain


async def input_letter_pos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # функция, которая принимает пользовательский ввод и сортирует его в соответствующие списки"
    try:
        take_letter_position = update.message.text
        # log.info(f'Пользователь - {update.effective_user.id} ввел: {take_letter_position}')
        letter_position = list(take_letter_position)
        for i in letter_position:
            if i == ' ':
                letter_position.remove(i)
        letter_position[0] = letter_position[0].lower()
        if (letter_position[0] not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
                or letter_position[1] not in '+-'
                or len(letter_position) > 3
                or len(letter_position) < 3):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=wrong_input_msg)
        elif (letter_position[1] == '+' and letter_position[2].isdigit() and int(letter_position[2]) <= 5):
            context.user_data["known_position"].append((letter_position[0], letter_position[2]))
        elif letter_position[1] == '-' and letter_position[2].isdigit() and int(letter_position[2]) <= 5:
            context.user_data["unknown_position"].append((letter_position[0], letter_position[2]))
        elif letter_position[1] == '-' and letter_position[2] == '-':
            context.user_data['letters_no'].append(letter_position[0])
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=wrong_input_msg)
    except Exception as exc:
        logMain.exception(f'Ошибка ввода пользователя {exc}, ввод {take_letter_position}, '
                          f'пользователь {update.effective_user.id}')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=wrong_input_msg)
