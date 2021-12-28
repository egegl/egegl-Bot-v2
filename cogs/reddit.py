import asyncpraw
import discord
import requests
import random
from asyncio import sleep
from discord.ext import commands
from __main__ import env


class RedditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        auth = requests.auth.HTTPBasicAuth(env["REDDIT_ID"], env["REDDIT_SECRET_KEY"])
        reddit_asyncpraw = asyncpraw.Reddit(
            client_id=env["REDDIT_ID"],
            client_secret=env["REDDIT_SECRET_KEY"],
            user_agent="<Discord:egegl-Bot:1.0>",
            username="egegl-Bot",
            password=env["REDDIT_PW"]
        )

        meme_subs = ["dankmemes", "memes", "comedyheaven"]
        upvote = "https://i.ibb.co/myHx28s/toppng-com-reddit-clipart-icon-reddit-upvote-transparent-1024x1049.png"

        @bot.command()
        async def memes(ctx, arg):
            for i in range(int(arg)):
                subreddit = await reddit_asyncpraw.subreddit(random.choice(meme_subs))
                submission_list = [submission async for submission in subreddit.hot(limit=20) if
                                   not submission.stickied and not submission.over_18 and not submission.spoiler]
                selector = random.randint(0, len(submission_list) - 1)
                p = submission_list[selector]
                reddit_embed = discord.Embed(title=str(p.title), url="https://reddit.com" + str(p.permalink),
                                             color=discord.Color.from_rgb(255, 69, 0))
                reddit_embed.set_footer(text=str(p.score), icon_url=upvote)
                reddit_embed.set_author(name="u/" + str(p.author), url="https://www.reddit.com/user/" + str(p.author))
                reddit_embed.set_image(url=p.url)
                await ctx.send(embed=reddit_embed)

        @bot.command()
        async def initmemes(ctx):
            if str(ctx.message.channel) == "memes":
                funny_embed = discord.Embed(description="✅ Initializing *the funny*... Expect to see memes!", color=discord.Color.from_rgb(255, 69, 0))
                await ctx.send(embed=funny_embed)
                while True:
                    await sleep(900)
                    subreddit = await reddit_asyncpraw.subreddit(random.choice(meme_subs))
                    submission_list = [submission async for submission in subreddit.hot(limit=15) if
                                       not submission.stickied and not submission.over_18 and not submission.spoiler]
                    selector = random.randint(0, len(submission_list) - 1)
                    p = submission_list[selector]
                    reddit_embed = discord.Embed(title=str(p.title), url="https://reddit.com" + str(p.permalink),
                                                 color=discord.Color.from_rgb(255, 69, 0))
                    reddit_embed.set_footer(text=str(p.score), icon_url=upvote)
                    reddit_embed.set_author(name="u/" + str(p.author),
                                            url="https://www.reddit.com/user/" + str(p.author))
                    reddit_embed.set_image(url=p.url)
                    await ctx.send(embed=reddit_embed)
            else:
                wrongchan_embed = discord.Embed(
                    description="**❌  Bu komut sadece adı *memes* olan yazı kanallarında kullanılabilir.**",
                    color=discord.Color.red())
                await ctx.send(embed=wrongchan_embed)
                return


def setup(bot):
    bot.add_cog(RedditCog(bot))
