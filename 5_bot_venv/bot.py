from config import config

BOT_TOKEN = config.bot_token.get_secret_value()

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters



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

async def show_all(update: Update, context: ContextTypes.DEFAULT_TYPE, n=250):
    words_list = []
    # get a list of all 5-letter words
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            words_list.append(line.rstrip())
    for i in [words_list[i:n + i] for i in range(0, len(words_list), n)]:
        message = ', '.join(i)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=(message))

def _no(word):
    # func that filter words that have not letters
    if len(letters_no) == 0:
        return True
    else:
        return not any([i in word for i in letters_no])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """func witch runs when /start command pressed"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=("Введите известные буквы и их позиции. \n\n"
                                         "Если известна правильная позиция,"
                                         " тогда через плюс (напр.: а+1 значит, что буква а на первом месте),"
                                         " если известна неправильная позиция, тогда через минус "
                                         "(напр.: я-5 значит, что буква я есть в слове и она точно не на 5 месте).\n\n"
                                         "Для окончания ввода, нажмите Enter. "
                                         "Если буквы нету ставите два минуса (напр.: ц--).\n\n"
                                         "Для выхода из программы наберите exit"))




async def main():
    result.clear()
    input_letter_pos()
    for word in words:
        w = word.strip().lower()
        if _no(w):
            if letter_position_filter(w):
                result.append(w)
    log.info(f'список отсутствующих букв - {letters_no}, '
             f'cписок букв с известными позициями - {known_position}, '
             f'список букв с неизвестными позициями - {unknown_position},'
             f'результат работы программы{result}')
    result



if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler(['start', 'help',], start)
    application.add_handler(start_handler)
    show_words_handler = CommandHandler(['words', ], show_all)
    application.add_handler(show_words_handler)


    application.run_polling()