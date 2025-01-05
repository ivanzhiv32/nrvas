from telebot import TeleBot

from app.constants import BASE_DIR
from app.handlers.start_command import StartCommand
from app.config import load_bot_secret


def main():
    bot_config = load_bot_secret()
    bot = TeleBot(
        token=bot_config.token,
    )

    start = StartCommand(
        bot=bot,
        dir_sticker=BASE_DIR / 'stickers/welcome_bender.tgs',
        id_admin=bot_config.id_admin
    )
    bot.message_handler(commands=["start"])(start)
    bot.polling()


if __name__ == "__main__":
    main()
