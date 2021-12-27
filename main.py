import os
import re
import ans
import wikipedia
import asyncpraw
import requests
import discord
import random
import youtube_dl
import asyncio
from urllib.request import Request, urlopen
from discord.ext import commands

bot = commands.Bot(command_prefix="!", help_command=None)

BOT_TOKEN = os.environ['BOT TOKEN']
YOUTUBE_KEY = os.environ['YOUTUBE KEY']
REDDIT_ID = os.environ['REDDIT ID']
REDDIT_SECRET_KEY = os.environ['REDDIT SECRET KEY']
REDDIT_PW = os.environ['REDDIT PW']

auth = requests.auth.HTTPBasicAuth(REDDIT_ID, REDDIT_SECRET_KEY)
reddit_asyncpraw = asyncpraw.Reddit(
    client_id=REDDIT_ID,
    client_secret=REDDIT_SECRET_KEY,
    user_agent="<Discord:egegl-Bot:1.0>",
    username="egegl-Bot",
    password=REDDIT_PW
)
reddit_asyncpraw.read_only = False

wikipedia.set_lang("en")
wikidil_str = "en"
queue_list = []
loading_embed = discord.Embed(description="*Cevabınız yükleniyor...*", color=discord.Color.blue())
sıra_boş_embed = discord.Embed(description="**▶️  Şarkı sırası boş.**", color=discord.Color.red())


@bot.event
async def on_guild_join(guild):
    joinchannel = guild.system_channel
    welcome_embed = discord.Embed(description=ans.welcome_message, color=discord.Color.blue())
    await joinchannel.send(embed=welcome_embed)


@bot.command()
async def p(ctx, *args):
    global vc, video_ids, FFMPEG_OPTIONS, YDL_OPTIONS
    search_term = ('{}'.format("+".join(args)))
    request = Request("https://www.youtube.com/results?search_query=" + search_term)
    request.add_header(BOT_TOKEN,
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    response = urlopen(request)
    video_ids = re.findall(r"watch\?v=(\S{11})", response.read().decode())
    queue_list.append("https://www.youtube.com/watch?v=" + video_ids[0])
    if len(queue_list) > 1:
        queue_embed = discord.Embed(
            description="**✅  Şarkı sıraya eklendi, şu an çalan şarkıyı geçmek için !skip yazın.**",
            color=discord.Color.red())
        await ctx.send(embed=queue_embed)
    voiceclient = ctx.guild.voice_client
    if not voiceclient:
        try:
            await ctx.author.voice.channel.connect()
        except:
            novoice_embed = discord.Embed(description="**❌  Bu komutu kullanmak için bir ses kanalına bağlanın.**",
                                          color=discord.Color.red())
            await ctx.send(embed=novoice_embed)
    vc = ctx.voice_client
    FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
    YDL_OPTIONS = {"format": "bestaudio"}
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(queue_list[0], download=False)
        url_2 = info["formats"][0]["url"]
        audio_source = await discord.FFmpegOpusAudio.from_probe(url_2, **FFMPEG_OPTIONS)
        if len(queue_list) == 1:
            vc.play(source=audio_source, after=lambda e: asyncio.run(skip(ctx)))
            await ctx.send("**Çalınan Parça: **" + " " + queue_list[0])


@bot.command()
async def dc(ctx):
    queue_list.clear()
    await ctx.voice_client.disconnect()


@bot.command()
async def skip(ctx):
    skip_embed = discord.Embed(description="**✅  Şarkı geçildi.**", color=discord.Color.red())
    try:
        del queue_list[0]
    except:
        return
    if len(queue_list) >= 1:
        vc.stop()
        connected = False
        while not connected:
            try:
                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(queue_list[0], download=False)
                    url_2 = info["formats"][0]["url"]
                    audio_source = await discord.FFmpegOpusAudio.from_probe(url_2, **FFMPEG_OPTIONS)
                    connected = True
                    await asyncio.sleep(1)
            except:
                pass
        vc.play(source=audio_source, after=lambda e: asyncio.run(skip(ctx)))
        await ctx.send(embed=skip_embed)
        await ctx.send("**Çalınan Parça: **https://www.youtube.com/watch?v=" + video_ids[0])
    elif len(queue_list) == 0:
        vc.stop()
        await ctx.send(embed=skip_embed)
        await ctx.send(embed=sıra_boş_embed)
        await asyncio.sleep(30)
        await vc.disconnect()
        return


@bot.command()
async def queue(ctx):
    a = 0
    if len(queue_list) > 0:
        sıra_embed = discord.Embed(title="**Şarkı Sırası:**", color=discord.Color.blue())
        await ctx.send(embed=sıra_embed)
        for i in queue_list:
            await ctx.send("**" + str(a + 1) + ")** " + queue_list[a])
            a += 1
    else:
        await ctx.send(embed=sıra_boş_embed)


@bot.command()
async def osu(ctx, arg):
    osu_full_link = ans.osu_link + arg
    with open("data/osulink.txt", "r+") as f:
        f.truncate(0)
        f.seek(0)
        f.write(osu_full_link)
    ans.osu_webscrape()
    osu_embed = discord.Embed(title=arg + " Adlı Kullanıcının osu! Profili", url=osu_full_link,
                              description=ans.osu_table, color=discord.Color.from_rgb(255, 20, 147))
    osu_embed.set_thumbnail(url=ans.osu_image)
    await ctx.send(embed=osu_embed)


@bot.command()
async def wikilang(ctx, arg):
    global wikidil_str
    if arg in wikipedia.languages():
        wikipedia.set_lang(arg)
        langsuccess_embed = discord.Embed(description="**✅  Wiki dili değiştirildi.**", color=discord.Color.blue())
        await ctx.send(embed=langsuccess_embed)
        wikidil_str = arg
    else:
        langerror_embed = discord.Embed(description=ans.langerror_desc, color=discord.Color.blue())
        await ctx.send(embed=langerror_embed)


@bot.command()
async def wiki(ctx, *args):
    arg = ('{}'.format(" ".join(args)))
    search_list = wikipedia.search(arg, 4, suggestion=False)
    search_embed = discord.Embed(title="Girilen Terim: *" + arg + "*",
                                 description="➤ Bu sayfalardan hangisini arıyorsunuz?\n➤ Cevabınızın yanındaki **numarayı** girin: \n",
                                 color=discord.Color.blue())
    search_embed.set_footer(text="(Wiki dili: " + wikidil_str.upper() + ")")
    await ctx.send(embed=search_embed)
    for i in search_list:
        ans.a += 1
        await ctx.send("**" + str(ans.a) + ") **" + i + "\n")
    ans.a = 0

    def check(m):
        return m.content is not None and m.channel == ctx.channel and any(i.isdigit() for i in str(m.content))

    message = await bot.wait_for('message', check=check)
    if message.author == ctx.author:
        await ctx.send(embed=loading_embed)
        topic_final_name = search_list[int(message.content) - 1]
        try:
            topic_final = wikipedia.page(topic_final_name, auto_suggest=False)
        except wikipedia.exceptions.DisambiguationError as e:
            s = e.options[0]
            topic_final = wikipedia.page(s, auto_suggest=False)
        topic_final_title = topic_final.title
        topic_final_summary = wikipedia.summary(topic_final_title, auto_suggest=False)
        if len(topic_final_summary) > 4096:
            long_embed = discord.Embed(
                description="**❌  Hata: İstenilen sayfa bir mesaja sığmayacak kadar uzun. Başka bir sayfa deneyin.**",
                color=discord.Color.red())
            await ctx.send(embed=long_embed)
            return
        else:
            wiki_embed = discord.Embed(title=topic_final_title, url=topic_final.url, description=topic_final_summary,
                                       color=discord.Color.blue())
            wiki_embed.set_author(name="Wikipedia " + wikidil_str.upper(), icon_url=ans.wikipedia_logo)
            wiki_embed.set_footer(text="(Wikipedia API'ının dilini değiştirmek için !wikilang)")
            if len(topic_final.images) > 0:
                wiki_embed.set_image(url=topic_final.images[0])
            await ctx.send(embed=wiki_embed)


@bot.command()
async def memes(ctx, arg):
    for i in range(int(arg)):
        subreddit = await reddit_asyncpraw.subreddit(random.choice(ans.meme_subs))
        submission_list = [submission async for submission in subreddit.hot(limit=20) if
                           not submission.stickied and not submission.over_18 and not submission.spoiler]
        selector = random.randint(0, len(submission_list) - 1)
        p = submission_list[selector]
        reddit_embed = discord.Embed(title=str(p.title), url="https://reddit.com" + str(p.permalink),
                                     color=discord.Color.from_rgb(255, 69, 0))
        reddit_embed.set_footer(text=str(p.score), icon_url=ans.reddit_upvote)
        reddit_embed.set_author(name="u/" + str(p.author), url="https://www.reddit.com/user/" + str(p.author))
        reddit_embed.set_image(url=p.url)
        await ctx.send(embed=reddit_embed)


@bot.command()
async def initmemes(ctx):
    if str(ctx.message.channel) == "memes":
        funny_embed = discord.Embed(description="✅ Initializing *the funny*... Expect to see memes!")
        await ctx.send(embed=funny_embed)
        while True:
            await asyncio.sleep(900)
            subreddit = await reddit_asyncpraw.subreddit(random.choice(ans.meme_subs))
            submission_list = [submission async for submission in subreddit.hot(limit=15) if
                               not submission.stickied and not submission.over_18 and not submission.spoiler]
            selector = random.randint(0, len(submission_list) - 1)
            p = submission_list[selector]
            reddit_embed = discord.Embed(title=str(p.title), url="https://reddit.com" + str(p.permalink),
                                         color=discord.Color.from_rgb(255, 69, 0))
            reddit_embed.set_footer(text=str(p.score), icon_url=ans.reddit_upvote)
            reddit_embed.set_author(name="u/" + str(p.author), url="https://www.reddit.com/user/" + str(p.author))
            reddit_embed.set_image(url=p.url)
            await ctx.send(embed=reddit_embed)
    else:
        wrongchan_embed = discord.Embed(
            description="**❌  Bu komut sadece adı *memes* olan yazı kanallarında kullanılabilir.**",
            color=discord.Color.red())
        await ctx.send(embed=wrongchan_embed)
        return


@bot.command()
async def megalul(ctx):
    megalul_embed = discord.Embed(title="**MEGALUL SMP**", url="https://bit.ly/30qiDXf",
                                  description="⬇️ **Minecraft Sunucumuza Katıl!**\nhttps://discord.gg/e6SY28AnXc",
                                  color=0xFF5733)
    megalul_embed.set_image(url="https://i.ibb.co/nfs61Jd/megalyl.png")
    await ctx.send(embed=megalul_embed)


@bot.command()
async def kur(ctx):
    ans.dolar_webscrape()
    dolar_embed = discord.Embed(color=discord.Color.green())
    dolar_embed.add_field(name="Dolar:", value=ans.dolar_kur + " ₺", inline=True)
    dolar_embed.add_field(name="Günlük Değişim:", value=ans.dolar_artis, inline=True)
    ans.euro_webscrape()
    euro_embed = discord.Embed(color=discord.Color.green())
    euro_embed.add_field(name="Euro:", value=ans.euro_kur + " ₺", inline=True)
    euro_embed.add_field(name="Günlük Değişim:", value=ans.euro_artis, inline=True)
    await ctx.send("**Güncel Dolar ve Euro Kuru 💸** \n ➤ Tarih: " + ans.dolar_tarih)
    await ctx.send(embed=dolar_embed)
    await ctx.send(embed=euro_embed)


@bot.command()
async def help(ctx):
    help_embed = discord.Embed(color=discord.Color.blue())
    help_embed.add_field(name="**▶️▶️ Genel Komutlar ◀️◀️**\n \u200b", value=ans.help_message_1, inline=False)
    help_embed.add_field(name="**▶️▶️ Müzik Komutları ◀️◀️**\n \u200b", value=ans.help_message_2, inline=False)
    help_embed.set_footer(icon_url="https://cdn.betterttv.net/emote/61526df6b63cc97ee6d3ab49/3x",
                          text="@egegl#8414 tarafından kodlandı.")
    await ctx.send(embed=help_embed)


bot.run(BOT_TOKEN)