import logging
import telegram


class TgLoggerHandler(logging.Handler):
    """
    A handler class which send error log to admin user.
    """

    def __init__(self, token: str, chat_id: int):
        super().__init__()
        self.chat_id = chat_id
        self.token = token

        self.bot = telegram.Bot(token=self.token)

    def emit(self, record):
        message = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=message)
