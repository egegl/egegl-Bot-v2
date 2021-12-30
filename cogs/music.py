import re
import discord
import youtube_dl
import asyncio
from discord.ext import commands
from urllib.request import Request, urlopen
from __main__ import env

FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                  "options": "-vn"}
YDL_OPTIONS = {"format": "bestaudio"}
queue_list = []
sıra_boş_embed = discord.Embed(description="**▶️  Şarkı sırası boş.**", color=discord.Color.red())
novoice_embed = discord.Embed(
    description="**❌  Bu komutu kullanmak için bir ses kanalına bağlanın.**",
    color=discord.Color.red())
samechan_embed = discord.Embed(
    description="**❌  Bu komutu kullanmak için botun olduğu ses kanalına bağlanın.**",
    color=discord.Color.red())
dc_embed = discord.Embed(
    description="**▶️  Ses kanalından çıkıldı.**",
    color=discord.Color.red())


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        async def yt_search():
            global currentvidlink
            request = Request("https://www.youtube.com/results?search_query=" + search_term)
            request.add_header(env["BOT_TOKEN"], "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ("
                                                 "KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
            response = urlopen(request)
            video_ids = re.findall(r"watch\?v=(\S{11})", response.read().decode())
            currentvidlink = "https://www.youtube.com/watch?v=" + video_ids[0]
            queue_list.append(currentvidlink)

        async def play():
            global audio_source
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url=queue_list[0], download=False)
                url_2 = info["formats"][0]["url"]
                audio_source = await discord.FFmpegOpusAudio.from_probe(url_2, **FFMPEG_OPTIONS)
                if len(queue_list) == 1:
                    vc.play(source=audio_source)
                elif len(queue_list) > 1:
                    queue_list.append(audio_source)

        @bot.command()
        async def self_check(ctx):
            while vc.is_playing():
                await asyncio.sleep(6)
            else:
                if len(queue_list) != 0:
                    await ctx.invoke(bot.get_command("skip"))
                else:
                    await asyncio.sleep(20)
                    await ctx.invoke(bot.get_command("dc"))

        @bot.command()
        async def p(ctx, *args):
            global queue_list, vc, search_term
            search_term = ('{}'.format("+".join(args)))
            if not ctx.guild.voice_client:
                try:
                    await ctx.author.voice.channel.connect()
                    vc = ctx.voice_client
                except:
                    await ctx.send(embed=novoice_embed)
                    return
            await yt_search()
            await play()
            if queue_list[0] == currentvidlink:
                await ctx.send("**Çalınan Parça:** " + str(queue_list[0]))
            else:
                queue_embed = discord.Embed(
                    description="**✅  Şarkı sıraya eklendi, şu an çalan şarkıyı geçmek için !skip yazın.**",
                    color=discord.Color.red())
                await ctx.send(embed=queue_embed)
            await ctx.invoke(bot.get_command("self_check"))

        @bot.command()
        async def dc(ctx):
            try:
                queue_list.clear()
                await ctx.voice_client.disconnect()
                await ctx.send(embed=dc_embed)
            except:
                return

        @bot.command()
        async def skip(ctx):
            if not ctx.author.voice.channel == ctx.guild.voice_client.channel:
                await ctx.send(embed=samechan_embed)
                return
            skip_embed = discord.Embed(description="**✅  Şarkı geçildi.**", color=discord.Color.red())
            try:
                del queue_list[0]
            except:
                return
            if len(queue_list) >= 1:
                vc.stop()
                connected = False
                while not connected:
                    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(url=queue_list[0], download=False)
                        url_2 = info["formats"][0]["url"]
                        audio_source = await discord.FFmpegOpusAudio.from_probe(url_2, **FFMPEG_OPTIONS)
                        connected = True
                vc.play(source=audio_source)
                await ctx.send(embed=skip_embed)
                await ctx.send("**Çalınan Parça:** " + str(queue_list[0]))
            elif len(queue_list) == 0:
                vc.stop()
                await ctx.send(embed=skip_embed)
                await ctx.send(embed=sıra_boş_embed)
                return
            await ctx.invoke(bot.get_command("self_check"))

        @bot.command()
        async def queue(ctx):
            try:
                if len(queue_list) > 0:
                    sıra_embed = discord.Embed(title="**Şarkı Sırası:**", color=discord.Color.red())
                    await ctx.send(embed=sıra_embed)
                    for i in range(len(queue_list)):
                        await ctx.send("**" + str(i + 1) + ")** " + queue_list[i])
                else:
                    await ctx.send(embed=sıra_boş_embed)
            except:
                return


def setup(bot):
    bot.add_cog(MusicCog(bot))
