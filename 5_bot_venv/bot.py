from config import config

BOT_TOKEN = config.bot_token.get_secret_value()

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ExtBot
from commands import commands

log = logging.getLogger('main_logger')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('main.log', 'a+', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

letters_no = []  # буквы которых нет
file = '5_words.txt'
result = []  # финальный результат
# words = get_words()  # доступный список слов
known_position = []  # буква и её известная позиция
unknown_position = []  # список букв с позициями, на которых их точно нет.




def _no(word):
    # func that filter words that have not letters
    if len(letters_no) == 0:
        return True
    else:
        return not any([i in word for i in letters_no])


def letter_position_filter(word):
    # func that filter words in according
    bool_filter_list = []  # список значений проверки позиций букв в слове, с двумя списками выше.
    for let in known_position:
        if int(let[1]) == word.find(let[0]) + 1:
            bool_filter_list.append(True)
        else:
            bool_filter_list.append(False)
    for let in unknown_position:
        if int(let[1]) == word.find(let[0]) + 1:
            bool_filter_list.append(False)
        elif word.find(let[0]) == -1:
            bool_filter_list.append(False)
        else:
            bool_filter_list.append(True)
    return all(bool_filter_list)


async def show_all(update: Update, context: ContextTypes.DEFAULT_TYPE, n=250):
    # get a list of all 5-letter words
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            w = line.strip().lower()
            if _no(w):
                if letter_position_filter(w):
                    result.append(w)
        log.info(f'список отсутствующих букв - {letters_no}, '
                 f'cписок букв с известными позициями - {known_position}, '
                 f'список букв с неизвестными позициями - {unknown_position},'
                 f'результат работы программы{result}')
        for i in [result[i:n + i] for i in range(0, len(result), n)]:
            message = ', '.join(i)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=(message))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """func witch runs when /start command pressed"""
    await context.bot.set_my_commands(commands=commands)  # меню команд
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=("Введите известные буквы и их позиции. \n\n"
                                         "Если известна правильная позиция,"
                                         " тогда через плюс (напр.: а+1 значит, что буква а на первом месте),"
                                         " если известна неправильная позиция, тогда через минус "
                                         "(напр.: я-5 значит, что буква я есть в слове и она точно не на 5 месте).\n\n"
                                         "Для окончания ввода, нажмите Enter. "
                                         "Если буквы нету ставите два минуса (напр.: ц--).\n\n"
                                         "Для выхода из программы наберите exit"))


async def input_letter_pos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # func that take from user letters

    try:
        take_letter_position = update.message.text
        log.info(f'Пользователь ввел: {take_letter_position}')
        letter_position = list(take_letter_position)
        for i in letter_position:
            if i == ' ':
                letter_position.remove(i)
        if len(letter_position) < 3:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=("Некорректный ввод. Пожалуйста прочитайте инструкцию."))

        letter_position[0] = letter_position[0].lower()
        if (letter_position[0] not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            or letter_position[1] not in '+-') or len(letter_position) > 3:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=("Некорректный ввод. Попробуйте еще, или прочитайте инструкцию."))
        elif (letter_position[1] == '+' and letter_position[2] != '+' and letter_position[2].isdigit()
              and int(letter_position[2]) <= 5):
            known_position.append((letter_position[0], letter_position[2]))
        elif (letter_position[1] == '-' and letter_position[2] != '-' and letter_position[2].isdigit()
              and int(letter_position[2]) <= 5):
            unknown_position.append((letter_position[0], letter_position[2]))
        elif letter_position[1] == '-' and letter_position[2] == '-':
            letters_no.append(letter_position[0])
    except Exception as exc:
        log.exception(f'Ошибка ввода пользователся {exc}, ввод {take_letter_position}')


async def clear_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    letters_no.clear()
    known_position.clear()
    unknown_position.clear()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=('Ваш ввод очищен. Начните заново. Для справки габерите /help.'))


async def main():
    result.clear()

    for word in words:
        w = word.strip().lower()
        if _no(w):
            if letter_position_filter(w):
                result.append(w)
    log.debug(f'список отсутствующих букв - {letters_no}, '
              f'cписок букв с известными позициями - {known_position}, '
              f'список букв с неизвестными позициями - {unknown_position},'
              f'результат работы программы{result}')
    result


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler(['start', 'help', ], start)
    application.add_handler(start_handler)
    show_words_handler = CommandHandler(['words', ], show_all)
    application.add_handler(show_words_handler)
    clear_handler = CommandHandler('clear_input', clear_input)
    application.add_handler(clear_handler)
    letter_input_hadler = MessageHandler(filters.TEXT & (~filters.COMMAND), input_letter_pos)
    application.add_handler(letter_input_hadler)


    application.run_polling()
