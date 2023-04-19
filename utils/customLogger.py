import logging
import time


class LogGen:
    @staticmethod
    def loggen():
        file_path = '.\\logs\\' + 'Automation_' + time.strftime("%Y%m%d-%H%M%S") + '.log'
        logger = logging.getLogger()
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(file_path, "w", encoding="UTF-8")

        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        logger = logging.getLogger()
        logger.setLevel(logging.ERROR)

        return logger
