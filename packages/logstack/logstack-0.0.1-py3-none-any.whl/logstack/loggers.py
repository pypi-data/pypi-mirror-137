from logstack.handlers import (
    file_logger,
    remote_logger,
)


class Logger(object):
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, url: str, port: str, log_name: str) -> None:
        # TODO: Check if this violates the singleton pattern. I should not be
        #       able to reconfigure the logger after it has been created.
        self.url = url
        self.port = port
        self.log_name = log_name

    def log_to_server():
        raise NotImplementedError

    def log_to_file():
        raise NotImplementedError


class DjangoLogger(Logger):
    pass


class FlaskLogger(Logger):
    pass


class FastApiLogger(Logger):
    pass