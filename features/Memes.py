import json
import random
import time

import requests
from discord.ext import commands

from Utility.Utils import *


class Memes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # FIXME: Fetching same memes sometimes
    @commands.command(name="meme")
    async def meme(self, ctx, arg1='dankmemes'):
        r = requests.get("https://www.reddit.com/r/{}.json?sort=top&t=year".format(arg1),
                         headers={'User-agent': 'All-In-Discord-Bot'})
        if r.status_code == 200:
            random.seed(time.time())
            for x in range(25):
                j = json.loads(r.text)
                index = random.randint(0, len(j['data']['children']) - 1)
                img_url = j['data']['children'][index]['data']['url']
                if img_url and ('.jpg' in img_url or '.png' in img_url or '.jpeg' in img_url):
                    await send(ctx.channel, title='Random image from subreddit \'{}\''.format(arg1), image=img_url)
                    return
            await send(ctx.channel, description='No random image found on subreddit \'{}\''.format(arg1))
        else:
            await send(ctx.channel, description='Subreddit not found or connection error')


def setup(bot: commands.Bot):
    bot.add_cog(Memes(bot))
