import os

from discord.ext import commands
from dotenv import load_dotenv

from Utility import Storage


def load_features():
    print('Loading features:')
    load_dotenv()
    base_path = os.path.join(os.path.dirname(__file__), 'features')
    files = os.listdir(base_path)

    for f in files:
        name = f.split('.')[0]
        if name.startswith('__') or name == 'Template':
            continue
        bot.load_extension('features.' + name)
        print('\t' + name + ' ✓')


if __name__ == '__main__':
    print("           _ _            _____                  ____        _   ")
    print("     /\   | | |          |_   _|                |  _ \      | |  ")
    print("    /  \  | | |  ______    | |  _ __    ______  | |_) | ___ | |_ ")
    print("   / /\ \ | | | |______|   | | | '_ \  |______| |  _ < / _ \| __|")
    print("  / ____ \| | |           _| |_| | | |          | |_) | (_) | |_ ")
    print(" /_/    \_\_|_|          |_____|_| |_|          |____/ \___/ \__|")

    bot = commands.Bot(command_prefix=Storage.get_prefix)
    load_features()
    print('Starting client')
    bot.run(os.getenv('TOKEN'))
