from discord.ext import commands


# Feature classes must implement the interface commands.Cog
class Template(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Receive the command !test like this
    @commands.command(name="test")
    async def test_command(self, ctx):
        # Do something here
        pass


# Setup function needed for registration of the feature Cog
def setup(bot: commands.Bot):
    bot.add_cog(Template(bot))