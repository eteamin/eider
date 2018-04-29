from os import path, getcwd
import yaml
from json import loads, JSONDecodeError


def load_config_file(test=False):
    conf = open(
        path.join(
            getcwd(), 'development.yml' if test is False else 'test.yml'
        ), 'r'
    )
    try:
        return yaml.load(conf)
    finally:
        conf.close()


def parse(data):
    try:
        return loads(data)
    except JSONDecodeError:
        return
