from features.FeaturesInterface import FeaturesInterface
import discord
import yaml


class Vote(FeaturesInterface):

    @staticmethod
    async def get_commands():
        return ["vote"]

    @staticmethod
    async def handle(client, message):
        if client is None or message is None:
            return
