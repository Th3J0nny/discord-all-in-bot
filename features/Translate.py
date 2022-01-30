from discord.ext import commands
from googletrans import Translator

# Feature classes must implement the interface commands.Cog
class Translate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Receive the command !test like this
    @commands.command(name="translate" aliases = ['tr'])
    async def translate(ctx,lang,*,args):
        lang = lang.lower();
        if lang not in googletrans.LANGUAGES and lang not in googletrans.LANGCODES:
            raise commands.BadArgument("Language DNE")

        translator = Translator()
        result = translator.translate(args, dest = lang)
        ctx.send(result.text)
        


# Setup function needed for registration of the feature Cog
def setup(bot: commands.Bot):
    bot.add_cog(Translate(bot))
