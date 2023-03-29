import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, Application, ContextTypes, CommandHandler, MessageHandler, filters

from commands import commands
from config import config, FILE

BOT_TOKEN = config.bot_token.get_secret_value()
ADMIN_ID = config.admin_id

log = logging.getLogger('main_logger')
log.setLevel(logging.INFO)
fh = logging.FileHandler('main.log', 'a+', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

async def post_start(appliсation: Application):
    # функция отправляет сообщение админу при запуске бота.
    await appliсation.bot.send_message(chat_id=ADMIN_ID,
                                   text="БОТ ЗАПУЩЕН!")

async def post_shutdown(appliсation: Application):
    # функция отправляет сообщение админу при запуске бота.
    await appliсation.bot.send_message(chat_id=ADMIN_ID,
                                   text="БОТ ОСТАНОВЛЕН!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #функция которая запускается при вводе команды /start
    context.user_data['letters_no'] = []  # буквы которых нет
    context.user_data["known_position"] = []  # буква и её известная позиция
    context.user_data['unknown_position'] = []  # список букв с позициями, на которых их точно нет.
    await context.bot.set_my_commands(commands=commands)  # меню команд
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=("Отправьте боту известные буквы и их позиции. \n\n"
                                         "Если известна <b>правильная позиция</b>,"
                                         " тогда через плюс '+' (напр.: <b>ф+1</b> значит, что буква 'а' на первом месте),"
                                         " если известна <b>неправильная позиция</b>, тогда через минус '-' "
                                         "(напр.: <b>я-5</b> значит, что буква 'я' есть в слове и она точно не на 5 месте).\n\n"
                                         "Если <b>буквы нет</b> ставите два минуса (напр.: <b>ц--</b>).\n\n"
                                         "Чтобы увидеть список слов введите /words, или воспользуйтесь MENU.\n\n"
                                         "Если Вы ошиблись при вводе, нажмите /clear_input, и попробуйте снова."),
                                   parse_mode='HTML')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    no_let_string = ', '.join(context.user_data['letters_no'])
    kn_let_string = '; '.join([f'<b>{tup[0]}</b> на {tup[1]} позиции' for tup in context.user_data['known_position']])
    unkn_let_string = '; '.join([f'<b>{tup[0]}</b> не на {tup[1]} позиции' for tup in context.user_data['unknown_position']])
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=("Отправьте боту известные буквы и их позиции. \n\n"
                                         "Если известна <b>правильная позиция</b>,"
                                         " тогда через плюс '+' (напр.: <b>ф+1</b> значит, что буква 'ф' на первом месте),"
                                         " если известна <b>неправильная позиция</b>, тогда через минус '-' "
                                         "(напр.: <b>я-5</b> значит, что буква 'я' есть в слове и она точно не на 5 месте).\n\n"
                                         "Если <b>буквы нет</b> ставите два минуса (напр.: <b>ц--</b>).\n\n"
                                         "Чтобы увидеть список слов введите /words, или воспользуйтесь MENU.\n\n"
                                         "Если Вы ошиблись при вводе, нажмите /clear_input, и попробуйте снова." +
                                         "\n\n На данный момент вы ввели:"
                                         f"\n\t - Буквы которых нет:\n\t\t {no_let_string}"
                                         f"\n\t - Известные буквы на известных позициях:\n\t\t  {kn_let_string}"
                                         f"\n\t - Буква точно есть, но пока не известно где:\n\t\t {unkn_let_string}"),
                                   parse_mode='HTML')


# TODO Разнести бота по модулям
# TODO сделать тестирование. слово для проверки скука


def extract_words(file):
    # функция которая получает список слов из файла. Один раз при запуске бота.
    words = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            w = line.strip().lower()
            words.append(w)
    return words


def _no(word, letters_no):
    # ф-я пропускает слова по списку букв которых нет в слове
    if len(letters_no) == 0:
        return True
    else:
        return not any([i in word for i in letters_no])


def letter_position_filter(word, known_position, unknown_position):
    # ф-я пропускает слова по спискам известных позиций и неизвестных
    letter_list = list(word)
    bool_filter_list = []  # список значений проверки позиций букв в слове.
    for let in known_position:
        kn_indexes_of_letters = [i + 1 for i, v in enumerate(letter_list) if let[0] == v]  # индексы встречающихся букв
        if len(kn_indexes_of_letters) == 0:
            bool_filter_list.append(False)
        else:
            for _ in kn_indexes_of_letters:
                if letter_list[int(let[1]) - 1] == let[0]:
                    bool_filter_list.append(True)
                else:
                    bool_filter_list.append(False)
    for let in unknown_position:
        unk_indexes_of_letters = [i for i, v in enumerate(letter_list) if let[0] == v]
        if len(unk_indexes_of_letters) == 0:
            bool_filter_list.append(False)
        else:
            for i in unk_indexes_of_letters:
                if i + 1 == int(let[1]):
                    bool_filter_list.append(False)
                else:
                    bool_filter_list.append(True)
    return all(bool_filter_list)


async def filter_words(update: Update, context: ContextTypes.DEFAULT_TYPE, n=250):
    # ф-я применяет фильтры для вывода слов
    result = []
    for w in words:
        if _no(w, context.user_data['letters_no']):
            if letter_position_filter(w, known_position=context.user_data['known_position'],
                                      unknown_position=context.user_data['unknown_position']):
                result.append(w)
    log.info(f'список отсутствующих букв - {context.user_data["letters_no"]}, '
             f'cписок букв с известными позициями - {context.user_data["known_position"]}, '
             f'список букв с неизвестными позициями - {context.user_data["unknown_position"]},')
    for i in [result[i:n + i] for i in range(0, len(result), n)]:
        message = ', '.join(i)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=message)


async def input_letter_pos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # функция, которая принимает пользовательский ввод и сортирует его в соответствующие списки
    wrong_input_message = "Некорректный ввод. Прочитайте инструкцию и попробуйте снова."
    try:
        take_letter_position = update.message.text
        log.info(f'Пользователь - {update.effective_user.id} ввел: {take_letter_position}')
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
                                           text=wrong_input_message)
        elif (letter_position[1] == '+' and letter_position[2].isdigit() and int(letter_position[2]) <= 5):
            context.user_data["known_position"].append((letter_position[0], letter_position[2]))
        elif letter_position[1] == '-' and letter_position[2].isdigit() and int(letter_position[2]) <= 5:
            context.user_data["unknown_position"].append((letter_position[0], letter_position[2]))
        elif letter_position[1] == '-' and letter_position[2] == '-':
            context.user_data['letters_no'].append(letter_position[0])
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=wrong_input_message)
    except Exception as exc:
        log.exception(f'Ошибка ввода пользователя {exc}, ввод {take_letter_position}, '
                      f'пользователь {update.effective_user.id}')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=wrong_input_message)


async def clear_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # очистка ввода пользователя
    context.user_data['letters_no'].clear()
    context.user_data["known_position"].clear()
    context.user_data["unknown_position"].clear()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=('Ваш ввод очищен. Начните заново. Для справки наберите /help.'))


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_start).post_stop(post_shutdown).build()
    words = extract_words(FILE)
    start_handler = CommandHandler(['start', ], start)
    application.add_handler(start_handler)
    help_handler = CommandHandler(['help', ], help)
    application.add_handler(help_handler)
    show_words_handler = CommandHandler(['words', ], filter_words)
    application.add_handler(show_words_handler)
    clear_handler = CommandHandler('clear_input', clear_input)
    application.add_handler(clear_handler)
    letter_input_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), input_letter_pos)
    application.add_handler(letter_input_handler)

    application.run_polling()
