import logging

class Log:
    def __init__(self):
        self.__logger = logging.getLogger(self.__class__.__name__)

        file_handler = logging.FileHandler('watcher.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_formatter)

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)
        self.__logger.setLevel(logging.DEBUG)

    def get_logger(self):
        return self.__logger