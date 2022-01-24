from discord.ext import commands

from utility import Storage
from utility.Utils import *

steps = dict()


def is_owner(message):
    return message.author.id == message.guild.owner_id


class Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='change-prefix', aliases=['changeprefix'])
    async def change_prefix(self, ctx, arg1):
        if is_owner(ctx):
            if arg1:
                Storage.set_prefix(ctx.guild.id, arg1)
                self.bot.command_prefix = arg1
                await send(ctx, description="Command prefix successfully changed to {}.".format(arg1))
            else:
                await send_error(ctx, description="Alias cannot be empty.")
        else:
            await send_error(ctx, description="Insufficient permissions. Please ask the server owner.")


    @commands.command(name='default-channel', aliases=['defaultchannel'])
    async def change_alone(self, ctx, arg1):
        if is_owner(ctx):
            if arg1 in await ctx.guild.fetch_channels():
                Storage.write(ctx.guild.id, "default_channel", arg1)
                await send(ctx, description="Default channel successfully set to {}.".format(arg1))
            else:
                await send_error(ctx, description="Target default channel does not exist.")
        else:
            await send_error(ctx, description="Insufficient permissions. Please ask the server owner.")


def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))
