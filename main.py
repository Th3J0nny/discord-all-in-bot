import os

from discord.ext import commands


def load_features():
    print('Loading features:')
    base_path = os.path.join(os.path.dirname(__file__), 'features')
    files = os.listdir(base_path)

    for f in files:
        name = f.split('.')[0]
        if name.startswith('__') or name == 'Template':
            continue
        bot.load_extension('features.' + name)
        print('\t' + name + ' ✓')


if __name__ == '__main__':
    bot = commands.Bot(command_prefix='!')
    load_features()
    print('Starting client')
    bot.run(os.getenv('TOKEN'))
