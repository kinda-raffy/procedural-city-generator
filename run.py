import logging.config


def setup():
    logging.config.fileConfig('log.conf')


def run(): pass


if __name__ == '__main__':
    setup()
    run()

_log_format: str = '[%(asctime)s ; %(name)s ; %(levelname)s] ~ %(message)s'
