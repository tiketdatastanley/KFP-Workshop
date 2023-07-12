from caelum.logger import logger_factory


def create_logger(name):
    options = logger_factory.get_options()
    options.set_name(name=name)
    return logger_factory.get_logger(options=options, debug=True)
