import logging


class Logger:
    def __init__(
        self, name: str = "web-scrapping-fastapi", log_to_file: bool = False, file_name: str = "app.log"
    ):
        self.name = name
        self.log_to_file = log_to_file
        self.file_name = file_name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Setting up the formatter
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Clear existing handlers to avoid duplication
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self._set_handler()

    def _set_handler(self):
        if self.log_to_file:
            file_handler = logging.FileHandler(self.file_name)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)

    def switch_to_file_logging(self, file_name: str = None):
        pass # future

    def switch_to_console_logging(self):
        self.log_to_file = False
        self._update_handler()

    def _update_handler(self):
        # Remove all handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        # Set new handler
        self._set_handler()

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)


# Usage
if __name__ == "__main__":
    # Initialize Logger, defaulting to console logging
    logger = Logger(name="MyApp")

    logger.info("This is an info message to the console")

    # Switch to file-based logging
    logger.switch_to_file_logging(file_name="my_app.log")
    logger.info("This is an info message to the file")

    # Switch back to console logging
    logger.switch_to_console_logging()
    logger.error("This is an error message to the console")
