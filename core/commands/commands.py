from telegram import BotCommand, Bot, BotCommandScopeDefault



commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Инструкция'
        ),
        BotCommand(
            command='clear_input',
            description='Очистить введенные буквы'
        ),
        BotCommand(
            command='words',
            description='Доступные слова'
        ),
    ]
