import logging.config


log_config = {
    "version": 1,
    "formatters": {
        "main_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "fh_letters_input": {
            "class": "logging.FileHandler",
            "formatter": "main_formatter",
            "filename": "logs/user_input.log"
        },
        "fh_commands_input": {
            "class": "logging.FileHandler",
            "formatter": "main_formatter",
            "filename": "logs/commands_input.log"
        },
        "fh_main": {
            "class": "logging.FileHandler",
            "formatter": "main_formatter",
            "filename": "logs/main.log"
        },
    },
    "loggers": {
        "usr_inp_log": {
            "handlers": ["fh_letters_input"],
            "level": "INFO",
        },
        "commands_inp_log": {
            "handlers": ["fh_commands_input"],
            "level": "INFO",
        },
        "main_log": {
            "handlers": ["fh_main"],
            "level": "WARNING",
        },
    }
}

logging.config.dictConfig(log_config)
logInput = logging.getLogger('usr_inp_log')
logCommands = logging.getLogger('commands_inp_log')
logMain = logging.getLogger('main_log')
