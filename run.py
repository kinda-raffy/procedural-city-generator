import logging.config
from typing import NoReturn
import generation.village as village


def set_logger() -> NoReturn:
    logging.config.fileConfig('log.conf')


def run() -> NoReturn:
    set_logger()
    village.Village(max_houses=200, max_grid_size=1000)


if __name__ == '__main__':
    run()
