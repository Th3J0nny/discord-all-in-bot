from features.FeaturesInterface import FeaturesInterface
import discord
import yaml


class Fun(FeaturesInterface):

    @staticmethod
    async def get_commands():
        return ["ping"]

    @staticmethod
    async def handle(client, message):
        if client is None or message is None:
            return
        if message.content == "!ping":
            await message.channel.send("pong")
