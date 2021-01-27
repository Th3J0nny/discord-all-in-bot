from features.FeaturesInterface import FeaturesInterface
import discord
import yaml


class MusicPlayer(FeaturesInterface):

    @staticmethod
    async def get_commands():
        return ["music"]

    @staticmethod
    async def handle(client, message):
        if client is None or message is None:
            return
