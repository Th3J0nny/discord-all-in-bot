import discord


async def send(channel, title='', description='', image='', color=0x4169E1):
    embed = discord.Embed(title=title, description=description, image=image, color=color)
    await channel.send(embed=embed)


async def send_error(channel, title='', description='', image=''):
    await send(channel, title=title, description=description, image=image, color=0xFF0000)


def is_this_bot(ctx):
    return ctx.author.id == 803637393143889980
