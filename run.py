import logging.config


def setup():
    logging.config.fileConfig('log.conf')


def run(): pass


if __name__ == '__main__':
    setup()
    run()
