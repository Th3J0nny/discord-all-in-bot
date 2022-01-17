import random

from discord.ext import commands

from utility.Utils import *


# TODO: Maybe replace this by simple !math cmd and using regex to detect math problem
class Math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx, *args):
        rand_min = 0
        rand_max = 100
        if len(args) == 1:
            try:
                rand_max = int(args[0])
            except ValueError:
                await send_error(ctx, description='Sorry, I don\'t know what number \'' + args[0] + '\' is.')
                return
        elif len(args) >= 2:
            try:
                rand_min = int(args[0])
                rand_max = int(args[1])
                if rand_max < rand_min:
                    await send_error(ctx, description='The first number has to be smaller than the second one.')
                    return
            except ValueError:
                await send_error(ctx, description='Please write two valid whole numbers.')
                return
        try:
            await send(ctx, title=random.randint(rand_min, rand_max))
        except ValueError:
            await send_error(ctx, description='Please write valid numbers.')

    @commands.command(name='add', aliases=['plus'])
    async def cmd_add(self, ctx, *args):
        if len(args) < 2:
            await send_error(ctx, description='Please provide at least 2 numbers')
            return
        res = 0
        for n in args:
            try:
                res += float(n)
            except ValueError:
                await send_error(ctx, description='Invalid number: {}'.format(n))
                return
        await send(ctx, title=str(res))

    @commands.command(name='sub', aliases=['subtract', 'minus'])
    async def cmd_sub(self, ctx, *args):
        if len(args) < 2:
            await send_error(ctx, description='Please provide at least 2 numbers')
            return
        try:
            res = float(args[0])
        except ValueError:
            await send_error(ctx, description='Invalid number: {}'.format(args[0]))
            return
        for n in args[1:]:
            try:
                res -= float(n)
            except ValueError:
                await send_error(ctx, description='Invalid number: {}'.format(n))
                return
        await send(ctx, title=str(res))

    @commands.command(name='mult', aliases=['multiply', 'multiplikation', 'multiplication'])
    async def cmd_mult(self, ctx, *args):
        if len(args) < 2:
            await send_error(ctx, description='Please provide at least 2 numbers')
            return
        res = 1
        for n in args:
            try:
                res *= float(n)
            except ValueError:
                await send_error(ctx, description='Invalid number: {}'.format(n))
                return
        await send(ctx, title=str(res))

    @commands.command(name='div', aliases=['divide', 'geteilt'])
    async def cmd_div(self, ctx, *args):
        if len(args) < 2:
            await send_error(ctx, description='Please provide at least 2 numbers')
            return
        try:
            res = float(args[0])
        except ValueError:
            await send_error(ctx, description='Invalid number: {}'.format(args[0]))
            return
        for n in args[1:]:
            try:
                res /= float(n)
            except ValueError:
                await send_error(ctx, description='Invalid number: {}'.format(n))
                return
        await send(ctx, title=str(res))


def setup(bot: commands.Bot):
    bot.add_cog(Math(bot))
