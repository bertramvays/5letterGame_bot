from telegram import Update
from telegram.ext import ContextTypes
from commands.commands import commands
from service_messages import *
from configs.config_log import logCommands


async def get_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Функция, которая запускается при вводе команды /start
    context.user_data['letters_no'] = []  # буквы которых нет
    context.user_data["known_position"] = []  # буква и её известная позиция
    context.user_data['unknown_position'] = []  # список букв с позициями, на которых их точно нет.
    context.bot_data[update.effective_user.id] = update.effective_user
    logCommands.info(f' Пользователь {update.effective_user.id} нажал /start')
    await context.bot.set_my_commands(commands=commands)  # меню команд
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=(start_msg),
                                   parse_mode='HTML')


async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    no_let_string = ', '.join(context.user_data['letters_no'])
    kn_let_string = '; '.join([f'<b>{tup[0]}</b> на {tup[1]} позиции' for tup in context.user_data['known_position']])
    unkn_let_string = '; '.join(
        [f'<b>{tup[0]}</b> не на {tup[1]} позиции' for tup in context.user_data['unknown_position']])
    logCommands.info(f' Пользователь {update.effective_user.id} нажал /help')
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=(start_msg + "\n\n На данный момент вы ввели:"
                                                     f"\n\t - Буквы которых нет:\n\t\t {no_let_string}"
                                                     f"\n\t - Известные буквы на известных позициях:\n\t\t{kn_let_string}"
                                                     f"\n\t - Буква точно есть, но пока не известно где:\n\t\t{unkn_let_string}"),
                                   parse_mode='HTML')
