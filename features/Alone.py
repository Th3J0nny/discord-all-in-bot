import distutils.util
from time import monotonic

from discord.ext import commands

from utility import Storage
from utility.Utils import *

steps = dict()


def is_owner(message):
    return message.author.id == message.guild.owner_id


# defines the text to send on loneliness detection
async def send_static(member, duration):
    threshold = Storage.read(member.guild.id, "duration")
    if threshold and duration < int(threshold):
        return
    channel_name = Storage.read(member.guild.id, "default_channel")
    channel = member.guild.system_channel
    if channel_name:
        channels = await member.guild.fetch_channels()
        for c in channels:
            if c.name == channel_name:
                channel = c
                break

    await send(channel, description="{} spent {} alone in a voice channel.".format(member.display_name,
                                                                                   float_to_time(duration)))


def float_to_time(duration):
    # because of monotonic clock, negative values may lead to unexpected behaviour
    # format only up to hours

    fmted = ""

    if duration > 3600:
        fmted += str(int(duration // 3600)) + " hours "
    if duration > 60:
        fmted += str(int(duration // 60) % 60) + " minutes "

    fmted += "{:.2f}".format(duration % 60) + " seconds"

    return fmted


async def check_from_empty_to_empty(source, target):
    if source is None or target is None:
        return False
    elif len(source.members) == 0 and len(target.members) == 1:
        return True
    else:
        return False


# A class that tracks how long someone spends alone in a voice channel
class Alone(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.users_alone = dict()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # read config and skip if feature is disabled
        alone_enabled = bool(Storage.read(member.guild.id, "alone_enabled"))
        if alone_enabled is None or not bool(alone_enabled):
            # feature not enabled, early exit
            return

        sendmsg = await check_from_empty_to_empty(before.channel, after.channel)

        if before.channel is not None:
            await self.check_source_channel(before.channel, member, sendmsg)

        # check nature of state update
        if after.channel is not None:
            await self.check_target_channel(after.channel, member, sendmsg)

    async def check_source_channel(self, channel, member, sendmsg):
        # left channel
        if len(channel.members) == 1:
            # member left, so somebody is alone now
            self.users_alone[channel.members[0].id] = monotonic()
        elif len(channel.members) == 0:
            # member was alone until now
            if member.id in set(self.users_alone):
                duration = monotonic() - self.users_alone.pop(member.id)

                if sendmsg:
                    return
                await send_static(member, duration)

    async def check_target_channel(self, channel, member, sendmsg):
        # joined channel
        if len(channel.members) == 1:
            # joined an empty channel
            self.users_alone[member.id] = monotonic()
        elif len(channel.members) == 2:
            # somebody joined channel where somebody was alone before
            inters = [i for i in channel.members if i.id in self.users_alone.keys()]
            # inters = set(channel.members).intersection(set(self.users_alone.keys()))
            # check if we 
            if len(inters) > 1:
                # unambiguous result
                for member in inters:
                    del self.users_alone[member.id]
            elif len(inters) == 1:
                # we have an exact record
                lonely_person = inters.pop()
                duration = monotonic() - self.users_alone.pop(lonely_person.id)

                if sendmsg:
                    return
                await send_static(lonely_person, duration)

    @commands.command(name='alone-status', aliases=['alonestatus'])
    async def alone_status(self, ctx, arg1):
        if is_owner(ctx):
            try:
                b = distutils.util.strtobool(arg1)
                Storage.write(ctx.guild.id, "alone_enabled", str(b))
                await send(ctx, description="Command Alone status successfully set to {}.".format(arg1))
            except ValueError:
                await send_error(ctx, description="Invalid value.")
        else:
            await send_error(ctx, description="Insufficient permissions. Please ask the server owner.")

    @commands.command(name='alone-channel', aliases=['alonechannel'])
    async def alone_channel(self, ctx, arg1):
        if is_owner(ctx):
            try:
                channel = await commands.TextChannelConverter().convert(ctx, arg1)
                Storage.write(ctx.guild.id, "default_channel", channel.name)
                await send(ctx, description="Default channel successfully set to {}.".format(channel.name))
                return
            except commands.ChannelNotFound:
                await send_error(ctx, description="Target default channel does not exist.")
        else:
            await send_error(ctx, description="Insufficient permissions. Please ask the server owner.")

    @commands.command(name='alone-duration', aliases=['aloneduration'])
    async def alone_duration(self, ctx, arg1):
        if is_owner(ctx):
            try:
                dur = int(arg1)
                if dur < 0:
                    await send_error(ctx, description="Number must be greater or equal 0.")
                    return
                Storage.write(ctx.guild.id, "duration", str(dur))
                await send(ctx, description="Only sending message when the person was in the channel alone for more "
                                            "than {} seconds.".format(dur))
                return
            except ValueError:
                await send_error(ctx, description="Invalid number. Please provide the duration in seconds.")
        else:
            await send_error(ctx, description="Insufficient permissions. Please ask the server owner.")


# Setup function needed for registration of the feature Cog
def setup(bot: commands.Bot):
    bot.add_cog(Alone(bot))
