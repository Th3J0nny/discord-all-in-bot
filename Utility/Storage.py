import inspect
from configparser import ConfigParser

config = ConfigParser()


def write(server_id, key, value):
    server = str(server_id)
    config.read('config.ini')
    if not config.has_section(server):
        config.add_section(server)
    config.set(server, '{}_{}'.format(get_caller_name(), key), value)
    with open('config.ini', 'w') as f:
        config.write(f)


def read(server_id, key):
    config.read('config.ini')
    return config.get(str(server_id), '{}_{}'.format(get_caller_name(), key), fallback=None)


def get_prefix(bot, message):
    config.read('config.ini')
    return config.get(str(message.guild.id), "PREFIX", fallback="!")


def set_prefix(server_id, prefix):
    server = str(server_id)
    config.read('config.ini')
    if not config.has_section(server):
        config.add_section(server)
    config.set(server, "PREFIX", prefix)
    with open('config.ini', 'w') as f:
        config.write(f)


def remove_entry(server_id, key):
    config.read('config.ini')
    if config.has_section(str(server_id)):
        config.remove_option(str(server_id), key)


def get_caller_name():
    stack = inspect.stack()
    count = 0
    while count < len(stack):
        try:
            return stack[count][0].f_locals["self"].__class__.__name__
        except KeyError:
            count += 1
