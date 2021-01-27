import discord
import os
import pkgutil
import asyncio

# Import features here
from features.Setup import Setup
from features.Vote import Vote
from features.MusicPlayer import MusicPlayer
from features.Fun import Fun


client = discord.Client()
commands = dict()


async def check_features():
    # Run feature checks
    print("Checking Features...")
    for p in pkgutil.iter_modules(['features']):
        if p.name == 'FeaturesInterface':
            continue
        try:
            await globals()[p.name].handle(None, None)
            feature_cmd = await globals()[p.name].get_commands()
        except Exception:
            raise NotImplementedError('Incorrect implementation of module \'' + p.name + '\'')
        if len(feature_cmd) == 0:
            raise NotImplementedError('Not commands specified for module \'' + p.name + '\'')
        for cmd in feature_cmd:
            if cmd in commands:
                raise NotImplementedError('Module \'' + p.name + '\' uses command \'' + cmd + '\' which is already in use by \'' + commands[cmd].__name__ + '\'')
            commands[cmd] = globals()[p.name]
        print("\t\'" + p.name + "\' -> OK")
    print("Features OK")


# Event Handler
@client.event
async def on_message(message):
    # Ensure we do not answer bot messages
    if (message.author.name != client.user.name
            and message.content.startswith('!')
            and message.content[1:] in commands):

        await commands[message.content[1:]].handle(client, message)


@client.event
async def on_guild_channel_delete(channel):
    # Delete Setup role if setup-channel gets deleted
    if channel.name == "setup-channel":
        setup_roles = [r for r in channel.guild.roles if r.name == "Setup"]
        if len(setup_roles) != 0:
            setup_role = setup_roles[0]
            await setup_role.delete()


# Run checks and start the client
asyncio.run(check_features())
print("Starting client")
client.run(os.getenv('TOKEN'))
