import logging
import logging.config
import yaml

with open('logger/config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
