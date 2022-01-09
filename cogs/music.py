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
cantplay_embed = discord.Embed(
    description="**❌  Bu şarkı çalınamıyor. Başka bir şarkı deneyin.**",
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
                try:
                    info = ydl.extract_info(url=queue_list[0], download=False)
                    url_2 = info["formats"][0]["url"]
                    audio_source = await discord.FFmpegOpusAudio.from_probe(url_2, **FFMPEG_OPTIONS)
                except:
                    del queue_list[0]
                    await play_context.send(embed=cantplay_embed)
                    return

        @bot.command()
        async def p(ctx, *args):
            global play_context
            play_context = ctx
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
            if queue_list[0] == currentvidlink:
                await play()
                vc.play(source=audio_source)
                await ctx.send("**Çalınan Parça:** " + currentvidlink)
            else:
                queue_embed = discord.Embed(
                    description="**✅  Şarkı sıraya eklendi, şu an çalan şarkıyı geçmek için !skip yazın.**",
                    color=discord.Color.red())
                await ctx.send(embed=queue_embed)
            await asyncio.sleep(3)
            if not ctx.voice_client.is_playing():
                await ctx.invoke(self.bot.get_command("skip"))

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
            skip_embed = discord.Embed(description="**✅  Şarkı geçildi.**", color=discord.Color.red())
            try:
                del queue_list[0]
            except:
                return
            await ctx.send(embed=skip_embed)
            if len(queue_list) >= 1:
                vc.stop()
                await play()
                vc.play(source=audio_source)
                await ctx.send("**Çalınan Parça:** " + currentvidlink)
            elif len(queue_list) == 0:
                vc.stop()
                await ctx.send(embed=sıra_boş_embed)
                await asyncio.sleep(30)
                if not ctx.voice_client.is_playing():
                    await ctx.invoke(self.bot.get_command("dc"))
                return

        @bot.command()
        async def queue(ctx):
            if len(queue_list) > 0:
                for i in range(len(queue_list)):
                    await ctx.send("**" + str(i + 1) + ")** " + queue_list[i])
            else:
                await ctx.send(embed=sıra_boş_embed)


def setup(bot):
    bot.add_cog(MusicCog(bot))
