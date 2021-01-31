import time

from discord.ext import commands

import Storage
from Utils import *

steps = dict()


class Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        steps['start'] = self.step_start
        steps['name'] = self.step_name_init
        # Further steps?
        steps['done'] = self.step_done

    @staticmethod
    async def start_step(ctx):
        curr_step = Storage.read(ctx.guild.id, 'step')
        await steps[curr_step](ctx)

    async def next_step(self, ctx):
        curr_step = Storage.read(ctx.guild.id, 'step')
        next_step = 'start'
        temp = iter(steps)
        for s in temp:
            if s == curr_step:
                next_step = next(temp, 'start')
        Storage.write(ctx.guild.id, 'step', next_step)
        await self.start_step(ctx)

    @staticmethod
    async def get_setup_channel(ctx):
        setup_channels = [c for c in ctx.guild.channels if c.name == 'setup-channel']
        if len(setup_channels) > 0:
            return setup_channels[0]
        return None

    async def step_start(self, ctx):
        user = ctx.author
        guild = ctx.guild
        setup_roles = [r for r in guild.roles if r.name == 'Setup']
        if len(setup_roles) == 0:
            setup_role = await guild.create_role(name='Setup')
        else:
            setup_role = setup_roles[0]
        await user.add_roles(setup_role)
        setup_channels = [c for c in guild.channels if c.name == 'setup-channel']
        if len(setup_channels) == 0:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                setup_role: discord.PermissionOverwrite(read_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            await guild.create_text_channel('setup-channel', overwrites=overwrites)
        else:
            setup_channel = setup_channels[0]
            await send(setup_channel, description='Hey ' + user.name + ', let\'s continue the setup over here.')
        await self.next_step(ctx)

    async def step_name_init(self, ctx):
        setup_channel = await self.get_setup_channel(ctx)
        await send(setup_channel, title=ctx.author.name + ' Welcome to the setup!',
                   description='Let\'s start with setting up the name of this bot...\n')
        time.sleep(.5)
        await send(setup_channel, title='How would you like to call me? Please don\'t be too mean ;)')

    async def step_done(self, ctx):
        setup_channel = await self.get_setup_channel(ctx)
        if setup_channel is None:
            await self.start_step(ctx)
        else:
            await send(setup_channel, title='You are done!',
                       description='Your Bot \'{}\' is now ready! You can close the setup and delete this channel by typing: **!close-setup**'.format(
                           Storage.read(ctx.guild.id, 'name')))

    @commands.command()
    async def setup(self, ctx):
        # Permission checks
        user = ctx.author
        if not user.guild_permissions.manage_guild:
            await send_error(ctx, description='You don\'t have the permission to use the setup')
            return
        await self.next_step(ctx)

    @commands.command(name='close-setup')
    async def close_setup(self, ctx):
        Storage.remove_entry(ctx.guild.id, 'step')
        setup_roles = [r for r in ctx.guild.roles if r.name == 'Setup']
        if len(setup_roles) != 0:
            setup_role = setup_roles[0]
            await setup_role.delete()
        if ctx.channel.name == 'setup-channel':
            await ctx.channel.delete()
            return
        setup_channels = [c for c in ctx.guild.channels if c.name == 'setup-channel']
        if len(setup_channels) > 0:
            await setup_channels[0].delete()

    @commands.Cog.listener(name='on_guild_channel_delete')
    async def on_guild_channel_delete(self, channel):
        # Delete Setup role if setup-channel gets deleted
        if channel.name == 'setup-channel':
            Storage.remove_entry(channel.guild.id, 'step')
            setup_roles = [r for r in channel.guild.roles if r.name == 'Setup']
            if len(setup_roles) != 0:
                setup_role = setup_roles[0]
                await setup_role.delete()

    @commands.Cog.listener(name='on_message')
    async def on_message(self, message):
        if message.author.id != 803637393143889980:
            setup_channel = await self.get_setup_channel(message)
            if setup_channel is not None and message.channel.id == setup_channel.id:
                curr_step = Storage.read(message.guild.id, 'step')
                if curr_step == 'name':
                    if len(message.content) > 32 or len(message.content) < 2:
                        await send_error(message.channel,
                                         description='The name must be between 2 and 32 characters long')
                    else:
                        Storage.write(message.guild.id, 'name', message.content)
                        await message.guild.me.edit(nick=message.content)
                        await send(message.channel, title='Feels nice to be {} now!'.format(message.content))
                        await self.next_step(message)

    @commands.command(name='change-name', aliases=['changename'])
    async def change_name(self, ctx, arg1):
        if len(arg1) > 32 or len(arg1) < 2:
            await send_error(ctx.channel,
                             description='The name must be between 2 and 32 characters long')
        else:
            Storage.write(ctx.guild.id, 'name', arg1)
            await ctx.guild.me.edit(nick=arg1)
            await send(ctx.channel, title='Feels nice to be {} now!'.format(arg1))

    @commands.command(aliases=['whatsyourname'])
    async def name(self, ctx):
        await send(ctx, title='You named me {}'.format(Storage.read(ctx.guild.id, 'name')))

def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))
