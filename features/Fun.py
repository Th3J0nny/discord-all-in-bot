from discord.ext import commands

from Utility.Utils import *


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await send(ctx, 'pong')

    @commands.command()
    async def hellothere(self, ctx):
        await send(ctx, title='General Kenobi')


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
