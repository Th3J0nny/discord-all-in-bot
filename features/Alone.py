from time import monotonic

from discord.ext import commands

from utility import Storage
from utility.Utils import *

steps = dict()


def is_owner(message):
    return message.author.id == message.guild.owner_id

# defines the text to send on loneliness detection
async def send_static(member, duration):
    channel = Storage.read(member.guild.id, "default_channel")
    if channel is None:
        channel = member.guild.system_channel

    await send(channel, description="{} spent {} seconds alone in a voice channel.".format(member.display_name,
                                                                                          duration))


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

        # check nature of state update
        if after.channel is not None:
            self.check_target_channel(after.channel, member)

        if before.channel is not None:
            self.check_source_channel(before.channel, member)

    async def check_source_channel(self, channel, member):
        # left channel
        if len(channel.members) == 1:
            # member left, so somebody is alone now
            self.users_alone[channel.members[0].id] = monotonic()
        elif len(channel.members) == 0:
            # member was alone until now
            if member.id in set(self.users_alone):
                duration = monotonic() - self.users_alone.pop(member.id)

                await send_static(member, duration)

    async def check_target_channel(self, channel, member):
        # joined channel
        if len(channel.members) == 1:
            # joined an empty channel
            self.users_alone[member.id] = monotonic()
        elif len(channel.members) == 2:
            # somebody joined channel where somebody was alone before
            inters = set(after.channel.members).intersection(set(self.users_alone.keys()))
            # check if we 
            if len(inters) > 1:
                # unambiguous result
                for member_id in inters:
                    del self.users_alone[member_id]
            elif len(inters) == 1:
                # we have an exact record
                lonely_person = inters.pop()
                duration = monotonic() - self.users_alone.pop(lonely_person)

                await send_static(member, duration)



    @commands.command(name='change-alone', aliases=['changealone'])
    async def change_alone(self, ctx, arg1):
        if is_owner(ctx):
            Storage.write(ctx.guild.id, "alone_enabled", arg1)
            await send(ctx, description="Command Alone status successfully set to {}.".format(bool(arg1)))
        else:
            await send_error(ctx, description="Insufficient permissions. Please ask the server owner.")


# Setup function needed for registration of the feature Cog
def setup(bot: commands.Bot):
    bot.add_cog(Alone(bot))
