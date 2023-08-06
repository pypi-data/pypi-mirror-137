import logging
import inspect


class CustomLogger:
    def log(file_name='file1.log', log_level=logging.DEBUG):
        # Set class/method name from where it is called
        logger_name = inspect.stack()[1][3]

        # Create logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        logger.handlers = []
        logger.propagate = False

        # Create file handler
        f = logging.FileHandler(file_name)

        # create formatter
        #formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s : %(message)s',
        #                              datefmt='%m/%d/%Y %I:%M:%S %p')

        # Add formatter to file handler
        f.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s : %(message)s'))

        logger.addHandler(f)

        return logger