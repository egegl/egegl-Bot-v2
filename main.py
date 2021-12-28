import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", help_command=None)

env = {
    "BOT_TOKEN": os.environ['BOT TOKEN'],
    "YOUTUBE_KEY": os.environ['YOUTUBE KEY'],
    "REDDIT_ID": os.environ['REDDIT ID'],
    "REDDIT_SECRET_KEY": os.environ['REDDIT SECRET KEY'],
    "REDDIT_PW": os.environ['REDDIT PW']
}

cogs = ["cogs.music",
        "cogs.soup",
        "cogs.wiki",
        "cogs.reddit",
        "cogs.help"
        ]

if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)


@bot.event
async def on_guild_join(guild):
    sys_channel = guild.system_channel
    welcome_embed = discord.Embed(description="▶ **Merhaba! Ben egegl Bot v2.** Beni Discord sunucunuza eklediğiniz "
                                              "için teşekkürler!\n\n▶ **!help** komutu ile işlevlerim hakkında bilgi "
                                              "edinebilirsiniz :)", color=discord.Color.blue())
    await sys_channel.send(embed=welcome_embed)



bot.run(env["BOT_TOKEN"])
