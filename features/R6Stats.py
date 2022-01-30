import json
import os

import requests
from discord.ext import commands

from utility.Utils import *


class StatsDBException(Exception):
    pass


class R6Rank(commands.Cog):

    def __init__(self, bot):
        self.auth = None
        self.bot = bot
        self.base_url = 'https://api.statsdb.net/r6/pc/player/{}'
        self.rank_image_url = 'https://api.statsdb.net/r6/assets/ranks/{}'
        self.check_and_setup_auth()

    def check_and_setup_auth(self):
        if os.getenv('STATSDB_USER_ID') and os.getenv('STATSDB_PW'):
            self.auth = (os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW'))
            return
        raise StatsDBException("Authentication with StatsDB failed. Missing USER_ID or PW")

    @commands.command(name="r6rank", description ="gets the rank of player")
    async def r6rank(self, ctx, arg1):
        r = requests.get(self.base_url.format(arg1), auth=(os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW')))
        if r.status_code == 200:
            stats = json.loads(r.text)
            rank = stats["payload"]["stats"]["seasonal"]["ranked"]["rank"]
            name = stats["payload"]["user"]["nickname"]
            mmr = stats["payload"]["stats"]["seasonal"]["ranked"]["mmr"]
            await send(ctx.channel, title="{} currently has {} MMR".format(name, mmr),
                       image=self.rank_image_url.format(rank))
        elif r.status_code == 429:
            await send_error(ctx.channel, description="Too many requests today. Try again tomorrow.")
        elif r.status_code == 404:
            await send_error(ctx.channel, description="Couldn't find player \"{}\"".format(arg1))
        else:
            await send_error(ctx.channel, description="Something went wrong.")

    @commands.command(name="r6kd", description ="gets the KD of player")
    async def r6kd(self, ctx, arg1):
        r = requests.get(self.base_url.format(arg1), auth=(os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW')))
        if r.status_code == 200:
            stats = json.loads(r.text)
            kills = stats["payload"]["stats"]["general"]["kills"]
            deaths = stats["payload"]["stats"]["general"]["deaths"]
            if deaths == 0:
                kd = 0
            else:
                kd = kills / deaths
            name = stats["payload"]["user"]["nickname"]
            await send(ctx.channel, title="{}'s general K/D is {:.2f}".format(name, kd))
        elif r.status_code == 429:
            await send_error(ctx.channel, description="Too many requests today. Try again tomorrow.")
        elif r.status_code == 404:
            await send_error(ctx.channel, description="Couldn't find player \"{}\"".format(arg1))
        else:
            await send_error(ctx.channel, description="Something went wrong.")

    @commands.command(name="r6wl", description ="gets the win-loss record of player")
    async def r6wl(self, ctx, arg1):
        r = requests.get(self.base_url.format(arg1), auth=(os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW')))
        if r.status_code == 200:
            stats = json.loads(r.text)
            wins = stats["payload"]["stats"]["general"]["wins"]
            losses = stats["payload"]["stats"]["general"]["losses"]
            if losses == 0:
                wl = 0
            else:
                wl = wins / losses
            name = stats["payload"]["user"]["nickname"]
            await send(ctx.channel, title="{}'s general W/L is {:.2f}".format(name, wl))
        elif r.status_code == 429:
            await send_error(ctx.channel, description="Too many requests today. Try again tomorrow.")
        elif r.status_code == 404:
            await send_error(ctx.channel, description="Couldn't find player \"{}\"".format(arg1))
        else:
            await send_error(ctx.channel, description="Something went wrong.")

    @commands.command(name="r6operatorkd", description ="gets the kill death ratio of player when using a certain operator")
    async def r6operatorkd(self, ctx, arg1, arg2):
        r = requests.get(self.base_url.format(arg1), auth=(os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW')))
        if r.status_code == 200:
            stats = json.loads(r.text)
            for op in stats["payload"]["stats"]["operators"]:
                if op["id"] == arg2:
                    kills = op["kills"]
                    deaths = op["deaths"]
                    if deaths == 0:
                        kd = 0
                    else:
                        kd = kills / deaths
                    name = stats["payload"]["user"]["nickname"]
                    await send(ctx.channel, title="{}'s K/D on {} is {:.2f}".format(name, arg2, kd))
                    return
            await send_error(ctx.channel, description="Couldn't find operator \"{}\"".format(arg2))
        elif r.status_code == 429:
            await send_error(ctx.channel, description="Too many requests today. Try again tomorrow.")
        elif r.status_code == 404:
            await send_error(ctx.channel, description="Couldn't find player \"{}\"".format(arg1))
        else:
            await send_error(ctx.channel, description="Something went wrong.")

    @commands.command(name="r6kdseasonal", description ="gets the kill death ratio of a player during the current season")
    async def r6kdseasonal(self, ctx, arg1):
        r = requests.get(self.base_url.format(arg1), auth=(os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW')))
        if r.status_code == 200:
            stats = json.loads(r.text)
            kills = stats["payload"]["stats"]["seasonal"]["ranked"]["kills"]
            deaths = stats["payload"]["stats"]["seasonal"]["ranked"]["deaths"]
            if deaths == 0:
                kd = 0
            else:
                kd = kills / deaths
            name = stats["payload"]["user"]["nickname"]
            await send(ctx.channel, title="{}'s seasonal K/D is {:.2f}".format(name, kd))
        elif r.status_code == 429:
            await send_error(ctx.channel, description="Too many requests today. Try again tomorrow.")
        elif r.status_code == 404:
            await send_error(ctx.channel, description="Couldn't find player \"{}\"".format(arg1))
        else:
            await send_error(ctx.channel, description="Something went wrong.")

    @commands.command(name="r6wlseasonal" description ="gets the winn loss record of a player during the current season")
    async def r6wlseasonal(self, ctx, arg1):
        r = requests.get(self.base_url.format(arg1), auth=(os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW')))
        if r.status_code == 200:
            stats = json.loads(r.text)
            wins = stats["payload"]["stats"]["seasonal"]["ranked"]["wins"]
            losses = stats["payload"]["stats"]["seasonal"]["ranked"]["losses"]
            if losses == 0:
                wl = 0
            else:
                wl = wins / losses
            name = stats["payload"]["user"]["nickname"]
            await send(ctx.channel, title="{}'s seasonal W/L is {:.2f}".format(name, wl))
        elif r.status_code == 429:
            await send_error(ctx.channel, description="Too many requests today. Try again tomorrow.")
        elif r.status_code == 404:
            await send_error(ctx.channel, description="Couldn't find player \"{}\"".format(arg1))
        else:
            await send_error(ctx.channel, description="Something went wrong.")

    @commands.command(name="r6operatorwl", description ="gets the win loss record of a player when using a certain operator")
    async def r6operatorwl(self, ctx, arg1, arg2):
        r = requests.get(self.base_url.format(arg1), auth=(os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW')))
        if r.status_code == 200:
            stats = json.loads(r.text)
            for op in stats["payload"]["stats"]["operators"]:
                if op["id"] == arg2:
                    wins = op["wins"]
                    losses = op["losses"]
                    if losses == 0:
                        wl = 0
                    else:
                        wl = wins / losses
                    name = stats["payload"]["user"]["nickname"]
                    await send(ctx.channel, title="{}'s W/L on {} is {:.2f}".format(name, arg2, wl))
                    return
            await send_error(ctx.channel, description="Couldn't find operator \"{}\"".format(arg2))
        elif r.status_code == 429:
            await send_error(ctx.channel, description="Too many requests today. Try again tomorrow.")
        elif r.status_code == 404:
            await send_error(ctx.channel, description="Couldn't find player \"{}\"".format(arg1))
        else:
            await send_error(ctx.channel, description="Something went wrong.")

    @commands.command(name="r6playtime", description = "gets the total play time of a player on R6")
    async def r6playtime(self, ctx, arg1):
        r = requests.get(self.base_url.format(arg1), auth=(os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW')))
        if r.status_code == 200:
            stats = json.loads(r.text)
            playtime = stats["payload"]["preview"][1]["value"]
            name = stats["payload"]["user"]["nickname"]
            await send(ctx.channel, title="{}'s total playtime is {}".format(name, playtime))
        elif r.status_code == 429:
            await send_error(ctx.channel, description="Too many requests today. Try again tomorrow.")
        elif r.status_code == 404:
            await send_error(ctx.channel, description="Couldn't find player \"{}\"".format(arg1))
        else:
            await send_error(ctx.channel, description="Something went wrong.")

    @commands.command(name="r6canweq", description="lets player know if they can queue")
    async def r6canweq(self, ctx, *args):
        if len(args) == 1:
            await send(ctx, description="Yes, you can queue alone Kappa")
            return
        if len(args) > 1:
            min_mmr = 9999999
            max_mmr = 0
            min_player = ""
            max_player = ""
            for player in args:
                r = requests.get(self.base_url.format(player),
                                 auth=(os.getenv('STATSDB_USER_ID'), os.getenv('STATSDB_PW')))
                if r.status_code == 200:
                    stats = json.loads(r.text)
                    name = stats["payload"]["user"]["nickname"]
                    mmr = stats["payload"]["stats"]["seasonal"]["ranked"]["mmr"]
                    if mmr > max_mmr:
                        max_mmr = mmr
                        max_player = name
                    if mmr < min_mmr:
                        min_mmr = mmr
                        min_player = name

                elif r.status_code == 429:
                    await send_error(ctx.channel, description="Too many requests today. Try again tomorrow.")
                elif r.status_code == 404:
                    await send_error(ctx.channel, description="Couldn't find player \"{}\"".format(player))
                else:
                    await send_error(ctx.channel, description="Something went wrong.")

            if max_mmr - min_mmr <= 1000:
                await send(ctx.channel, title="You can queue together!")
            else:
                await send(ctx.channel, title="You can NOT queue together!",
                           description="Lowest player: {} ({} MMR)\nHighest player: {} ({} MMR)\nDifference: {} MMR".format(
                               min_player,
                               min_mmr,
                               max_player,
                               max_mmr,
                               (max_mmr - min_mmr)))


def setup(bot: commands.Bot):
    bot.add_cog(R6Rank(bot))
