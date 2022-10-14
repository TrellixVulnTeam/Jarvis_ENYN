from logging import *

ACTION = INFO + 1
ENGAGE = WARNING + 1


class MyLogger(Logger):
    def action(self, msg, *args, **kwargs):
        if self.isEnabledFor(ACTION):
            self._log(ACTION, msg, args, **kwargs)

    def engage(self, msg, *args, **kwargs):
        if self.isEnabledFor(ENGAGE):
            self._log(ENGAGE, msg, args, **kwargs)


class StreamHandlerFormatter(Formatter):

    def formatException(self, ei) -> str:
        return ""


logger: MyLogger = MyLogger(MyLogger.__name__)

info = logger.info
critical = logger.critical
error = logger.error
fatal = logger.fatal
warning = logger.warning
debug = logger.debug
action = logger.action
engage = logger.engage
exception = logger.exception


def __fmt_filter(record):
    record.levelname = f"[{record.levelname.center(9, ' ')}]"
    return True


def configure_log():
    basicConfig(level=DEBUG)

    addLevelName(ACTION, "ACTION")
    addLevelName(ENGAGE, "ENGAGE")

    date_format: str = "%d.%m.%Y %H:%M:%S"

    stream_logger_formatting: Formatter = StreamHandlerFormatter("%(asctime)-20s %(levelname)s %(message)s",
                                                                 datefmt=date_format)
    file_logger_formatting: Formatter = Formatter(
        "%(asctime)-20s %(levelname)s [%(filename)-20s:%(lineno)d] %(message)s", datefmt=date_format)

    stream_handler = StreamHandler()
    stream_handler.setLevel(INFO)
    stream_handler.setFormatter(stream_logger_formatting)

    file_logger = FileHandler("speech-assistant.log")
    file_logger.setLevel(DEBUG)
    file_logger.setFormatter(file_logger_formatting)

    logger.addHandler(stream_handler)
    logger.addHandler(file_logger)

    logger.addFilter(__fmt_filter)
