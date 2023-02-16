from telegram import KeyboardButton, ReplyKeyboardMarkup

commands = ['start', 'help', 'clear', 'words']
button_list = [[KeyboardButton(comm)] for comm in commands]
reply_markup = ReplyKeyboardMarkup(button_list)
