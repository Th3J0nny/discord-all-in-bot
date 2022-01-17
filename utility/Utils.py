import discord


async def send(channel, title='', description='', image='', color=0x4169E1):
    embed = discord.Embed(title=title, description=description, color=color)
    if image:
        embed.set_image(url=image)
    await channel.send(embed=embed)


async def send_error(channel, title='', description='', image=''):
    await send(channel, title=title, description=description, image=image, color=0xFF0000)


def is_bot(author):
    return author.bot
