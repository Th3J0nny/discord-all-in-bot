from features.FeaturesInterface import FeaturesInterface
import discord
import yaml


class Setup(FeaturesInterface):

    @staticmethod
    async def get_commands():
        return ["setup"]

    @staticmethod
    async def handle(client, message):
        if client is None or message is None:
            return
        user = message.author
        if not user.guild_permissions.manage_guild:
            await message.channel.send('You don\'t have the permission to start the setup')
            return
        guild = message.guild
        setup_roles = [r for r in guild.roles if r.name == "Setup"]
        if len(setup_roles) == 0:
            setup_role = await guild.create_role(name="Setup")
        else:
            setup_role = setup_roles[0]
        await user.add_roles(setup_role)
        setup_channels = [c for c in guild.channels if c.name == "setup-channel"]
        if len(setup_channels) == 0:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                setup_role: discord.PermissionOverwrite(read_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            setup_channel = await guild.create_text_channel('setup-channel', overwrites=overwrites)
            await message.channel.send('Starting setup...')
            await setup_channel.send(user.mention + ' Welcome to the setup!')
        else:
            setup_channel = setup_channels[0]
            await setup_channel.send('Hey ' + user.mention + ', let\'s continue the setup over here.')