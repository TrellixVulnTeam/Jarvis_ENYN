import logging


def configure_logging():
    logging.basicConfig(
        format="%(asctime)-30s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        filename="speech-assistant.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    logging.getLogger().addHandler(MyStreamHandler())
    file_logger = MyFileHandler("speech-assistant.log")
    file_logger.setLevel(logging.DEBUG)
    file_logger_formatting = logging.Formatter("%(asctime)-30s %(threadName)-12s %(levelname)-8s %(message)s")
    file_logger.setFormatter(file_logger_formatting)
    logging.getLogger().addHandler(file_logger)


def format_message(record):
    new_message = record.getMessage().split("]")
    return new_message[0].rjust(15) + new_message[1]


class MyStreamHandler(logging.StreamHandler):
    def emit(self, record):
        record.message = format_message(record)
        super().emit(record)


class MyFileHandler(logging.FileHandler):
    def emit(self, record):
        record.message = format_message(record)
        super().emit(record)
