import logging

module = ''


def config_log(file, set_module):
    global module
    module = set_module
    logging.basicConfig(filename=file,
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s'
                        )


def log(message):
    global module
    logging.info(f"{module}: {message}")
