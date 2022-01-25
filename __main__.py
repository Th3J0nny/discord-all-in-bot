import argparse
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utility import Storage


def load_features():
    print('Loading features:')
    load_dotenv()
    base_path = os.path.join(os.path.dirname(__file__), 'features')
    files = os.listdir(base_path)

    for f in files:
        name = f.split('.')[0]
        if name.startswith('__') or name == 'Template':
            continue
        if name.lower() in excluded_features:
            print('\t' + name + ' X')
            continue
        bot.load_extension('features.' + name)
        print('\t' + name + ' ✓')


if __name__ == '__main__':
    print("\nWelcome to the one and only")
    print("           _ _            _____                  ____        _   ")
    print("     /\   | | |          |_   _|                |  _ \      | |  ")
    print("    /  \  | | |  ______    | |  _ __    ______  | |_) | ___ | |_ ")
    print("   / /\ \ | | | |______|   | | | '_ \  |______| |  _ < / _ \| __|")
    print("  / ____ \| | |           _| |_| | | |          | |_) | (_) | |_ ")
    print(" /_/    \_\_|_|          |_____|_| |_|          |____/ \___/ \__|\n")

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--exclude-features', nargs='*', default=[], help="Use this to exclude one or more "
                                                                                "features when starting the bot.")

    args = vars(parser.parse_args())
    excluded_features = [name.lower() for name in args['exclude_features']]

    intents = discord.Intents.default()
    intents.voice_states = True
    bot = commands.Bot(command_prefix=Storage.get_prefix, intents=intents)
    load_features()
    print('Bot is running...')
    bot.run(os.getenv('TOKEN'))
