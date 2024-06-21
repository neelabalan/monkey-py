import logging
import logging.config

import tomllib


def setup_logging(path: str = 'log.toml', default_level: int = logging.INFO):
    with open(path, 'rb') as _file:
        try:
            config = tomllib.load(_file)
            logging.config.dictConfig(config)
        except Exception as e:
            print(f'Error in Logging Configuration. Using default configs: {e}')
            logging.basicConfig(level=default_level)
    return logging.getLogger()


setup_logging()
