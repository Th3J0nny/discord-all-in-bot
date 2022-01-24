from discord.ext import commands

from utility import Storage
from utility.Utils import *

from time import monotonic 

steps = dict()

# A class that tracks how long someone spends alone in a voice channel
class Alone(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.users_alone = dict()

    # Receive the command !test like this
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # read config and skip if feature is disabled
        alone_enabled = Storage.read(member.guild.id, "alone_enabled")
        if alone_enabled is None or ! bool(alone_enabled):
            return

        # check nature of state update
        if before.channel is None and after.channel is not None:
            # joined channel
            if len(after.channel.members) == 1:
                # alone
                self.users_alone[member.id] = monotonic()
            elif len(after.channel.members) == 2:
                # somebody joined channel where somebody was alone before
                inters = set(after.channel.members).intersect(set(self.users_alone.keys()))
                # check if we 
                if len(inters) > 1:
                    # unambiguous result
                    for member_id in inters:
                        del self.users_alone[member_id]
                elif len(inters) == 1:
                    # we have an exact record
                    lonely_person = inters.pop()
                    duration = monotonic() - self.users_alone.pop(lonely_person)

                    channel = member.guild.system_channel
                    if channel is None:
                        # channel not available
                        return

                    send(channel, description="User {} spent {} alone in a voice channel".format(member.guild.get_member(lonely_person).display_name, duration))



        elif before.channel is not None and after.channel is None:
            # left channel
            if len(before.channel.members) == 1:
                # member left, so somebody is alone now
                self.users_alone[before.channel.members[0].id] = monotonic()
            elif len(before.channel.members) == 0:
                # member was alone until now
                if member.id in set(self.users_alone):
                    duration = monotonic() - self.users_alone.pop(member.id)

                    channel = member.guild.system_channel
                    if channel is None:
                        # channel not available
                        return

                    send(channel, description="User {} spent {} alone in a voice channel".format(member.display_name, duration))



    @commands.command(name='change-alone', aliases=['changealone'])
    async def change_alone(self, ctx, arg1):
        if is_owner(ctx):
            Storage.write(ctx.guild.id, bool(arg1))
            await send(ctx, description="Command Alone status successfully set to {}.".format(bool(arg1)))
        else:
            await send_error(ctx, description="Insufficient permissions. Please ask the server owner")


# Setup function needed for registration of the feature Cog
def setup(bot: commands.Bot):
    bot.add_cog(Alone(bot))
